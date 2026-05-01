import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.database import Base, get_db
from backend.main import app

TEST_DB_URL = "sqlite:///./data/test.db"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def _register(username="testuser"):
    return client.post("/users/register", json={"username": username, "password": "pass"})


def test_submit_and_retrieve_score():
    user_id = _register().json()["data"]["id"]
    resp = client.post(f"/scores/{user_id}", json={"value": 42})
    assert resp.status_code == 200
    assert resp.json()["data"]["value"] == 42


def test_leaderboard_returns_top_scores():
    uid1 = _register("alice").json()["data"]["id"]
    uid2 = _register("bob").json()["data"]["id"]
    client.post(f"/scores/{uid1}", json={"value": 10})
    client.post(f"/scores/{uid2}", json={"value": 99})
    resp = client.get("/scores/leaderboard")
    entries = resp.json()["data"]
    assert entries[0]["username"] == "bob"
    assert entries[0]["rank"] == 1
