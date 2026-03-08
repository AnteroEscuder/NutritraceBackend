from sqlalchemy import Column, Integer, String, Text, DateTime, func, Index
from app.database import Base


class CommunityMessage(Base):
    __tablename__ = "community_messages"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(String(50), index=True, nullable=False, default="general")

    user_id = Column(Integer, index=True, nullable=False)
    user_name = Column(String(120), nullable=False)

    text = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    __table_args__ = (
        Index("ix_community_room_created", "room_id", "created_at"),
    )
