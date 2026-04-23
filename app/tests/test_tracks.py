import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app

client = TestClient(app)

def test_get_tracks_status():
    mock_db = MagicMock()
    mock_db.execute.return_value.fetchall.return_value = []
    with patch("app.routes.tracks.get_db", return_value=iter([mock_db])):
        res = client.get("/api/tracks/")
        assert res.status_code == 200

def test_search_tracks():
    mock_db = MagicMock()
    mock_db.execute.return_value.fetchall.return_value = []
    with patch("app.routes.tracks.get_db", return_value=iter([mock_db])):
        res = client.get("/api/tracks/?q=Love")
        assert res.status_code == 200