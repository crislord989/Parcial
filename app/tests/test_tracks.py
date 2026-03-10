import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    res = client.get("/")
    assert res.status_code == 200

def test_root_message():
    res = client.get("/")
    assert res.json()["message"] == "Chinook API funcionando"
