import os

os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db

from app.models.user import User
from app.models.food import Food
from app.models.allergen import Allergen
from app.models.food_allergen import FoodAllergen
from app.models.meal import Meal
from app.models.goal import Goal
from app.models.community_message import CommunityMessage
from app.models.user_allergen import UserAllergen
from app.main import app


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture()
def auth_headers(client):
    def _auth_headers(email="ana@example.com", password="secret123", name="Ana"):
        client.post(
            "/auth/register",
            json={"name": name, "email": email, "password": password},
        )
        response = client.post(
            "/auth/login",
            data={"username": email, "password": password},
        )
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

    return _auth_headers
