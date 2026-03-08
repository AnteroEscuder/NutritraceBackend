import json
from typing import Dict, Set, Optional

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.database import get_db
from app.models.community_message import CommunityMessage
from app.schemas.message import CommunityMessageOut
from app.utils.security import get_current_user, get_current_user_from_token

router = APIRouter(prefix="/community", tags=["Community"])

ROOM_CONNECTIONS: Dict[str, Set[WebSocket]] = {}


def ws_add(room_id: str, ws: WebSocket):
    ROOM_CONNECTIONS.setdefault(room_id, set()).add(ws)


def ws_remove(room_id: str, ws: WebSocket):
    if room_id in ROOM_CONNECTIONS:
        ROOM_CONNECTIONS[room_id].discard(ws)
        if not ROOM_CONNECTIONS[room_id]:
            ROOM_CONNECTIONS.pop(room_id, None)


async def broadcast(room_id: str, event: str, data: dict):
    conns = list(ROOM_CONNECTIONS.get(room_id, set()))
    if not conns:
        return

    payload = json.dumps({"event": event, "data": data}, default=str)
    dead = []

    for ws in conns:
        try:
            await ws.send_text(payload)
        except Exception:
            dead.append(ws)

    for ws in dead:
        ws_remove(room_id, ws)


@router.get("/messages", response_model=list[CommunityMessageOut])
def get_messages(
    room_id: str = Query(default="general"),
    limit: int = Query(default=50, ge=1, le=200),
    before_id: Optional[int] = Query(default=None),
    db: Session = Depends(get_db),
    _current_user=Depends(get_current_user),
):
    q = db.query(CommunityMessage).filter(CommunityMessage.room_id == room_id)

    if before_id is not None:
        q = q.filter(CommunityMessage.id < before_id)

    rows = q.order_by(desc(CommunityMessage.id)).limit(limit).all()
    return list(reversed(rows))


def get_token_from_ws(websocket: WebSocket) -> Optional[str]:
    # 1) query param ?token=
    token = websocket.query_params.get("token")
    if token:
        return token

    # 2) header Authorization
    auth = websocket.headers.get("authorization")
    if auth and auth.lower().startswith("bearer "):
        return auth.split(" ", 1)[1]

    return None


@router.websocket("/ws")
async def community_ws(websocket: WebSocket, db: Session = Depends(get_db)):
    """
    WS protocol:
    client -> { event: "join_room", data: { room_id } }
    client -> { event: "new_message", data: { text } }
    server -> { event: "message_created", data: { ...message } }
    """
    await websocket.accept()

    # auth
    token = get_token_from_ws(websocket)
    if not token:
        await websocket.close(code=4401)
        return

    try:
        user = get_current_user_from_token(token, db)
    except Exception:
        await websocket.close(code=4401)
        return

    # room default
    room_id = "general"
    ws_add(room_id, websocket)

    try:
        await websocket.send_text(
            json.dumps(
                {
                    "event": "connected",
                    "data": {"room_id": room_id, "user": {"id": user.id, "name": user.name}},
                }
            )
        )

        while True:
            raw = await websocket.receive_text()
            msg = json.loads(raw or "{}")
            event = msg.get("event")
            data = msg.get("data") or {}

            if event == "join_room":
                new_room = (data.get("room_id") or "general").strip()[:50]
                if new_room != room_id:
                    ws_remove(room_id, websocket)
                    room_id = new_room
                    ws_add(room_id, websocket)
                    await websocket.send_text(
                        json.dumps({"event": "joined", "data": {"room_id": room_id}})
                    )

            elif event == "new_message":
                text = (data.get("text") or "").strip()
                if not text:
                    continue
                if len(text) > 2000:
                    text = text[:2000]

                m = CommunityMessage(
                    room_id=room_id,
                    user_id=user.id,
                    user_name=user.name,
                    text=text,
                )
                db.add(m)
                db.commit()
                db.refresh(m)

                payload = {
                    "id": m.id,
                    "room_id": m.room_id,
                    "user_id": m.user_id,
                    "user_name": m.user_name,
                    "text": m.text,
                    "created_at": m.created_at.isoformat() if m.created_at else None,
                }
                await broadcast(room_id, "message_created", payload)

            elif event == "ping":
                await websocket.send_text(json.dumps({"event": "pong", "data": {}}))

    except WebSocketDisconnect:
        pass
    finally:
        ws_remove(room_id, websocket)
        try:
            await websocket.close()
        except Exception:
            pass
