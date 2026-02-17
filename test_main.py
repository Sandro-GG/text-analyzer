import pytest
from fastapi.testclient import TestClient
from main import app
from sqlalchemy.orm import sessionmaker
import sqlalchemy as sa
from database import get_db, Base

db = sa.create_engine(
    "sqlite:///:memory:",
    connect_args={
        "check_same_thread": False,
    },
    poolclass=sa.StaticPool
)
TestingSession = sessionmaker(bind=db)

def override_get_db():
    db_session = TestingSession()
    try:
        yield db_session
    finally:
        db_session.close()

client = TestClient(app)
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=db)
    yield
    Base.metadata.drop_all(bind=db)

def test_create_analysis():
    payload = {
        "text": "I am testing this thing, hope it works"
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["content"] == "I am testing this thing, hope it works"
    assert data["word_count"] == 8

def test_text_too_large():
    large_text = "a" * 10001
    payload = {
        "text": large_text
    }
    response = client.post("/analyze", json=payload)
    data = response.json()
    
    assert response.status_code == 413
    assert data["detail"] == "Payload Too Large"
    
def test_update_entry():
    payload = {
        "text": "I am testing this thing, hope it works"
    }
    response = client.post("/analyze", json=payload)
    data = response.json()
    id = data["id"]
    
    payload = {
        "text": "Hope it changes to this now"
    }
    response = client.put(f"/id/{id}", json=payload)
    data = response.json()
    
    assert response.status_code == 200
    assert data["content"] == "Hope it changes to this now"
    assert data["word_count"] == 6
    
def test_delete_entry():
    payload = {
        "text": "I am testing this thing, hope it works"
    }
    response = client.post("/analyze", json=payload)
    data = response.json()
    id = data["id"]
    
    response = client.delete(f"/id/{id}")
    response = client.get("/history")
    data = response.json()
    
    existing_ids = [entry["id"] for entry in data]
    
    assert id not in existing_ids
    
def test_get_history():
    texts = ["This is first", "This is second", "And this is third"]
    for t in texts:
        client.post("/analyze", json={"text": t})
    
    response = client.get("/history?limit=2")
    data = response.json()
    
    assert response.status_code == 200
    assert len(data) == 2