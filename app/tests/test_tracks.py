from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from app.main import app
from app.database import get_db

def override_get_db():
    mock_db = MagicMock()
    mock_db.execute.return_value.fetchall.return_value = []
    yield mock_db

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_get_tracks_status():
    res = client.get("/api/tracks/")
    assert res.status_code == 200

def test_search_tracks():
    res = client.get("/api/tracks/?q=Love")
    assert res.status_code == 200
