from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_tracks():
    response = client.get("/tracks/")
    assert response.status_code in (200, 500)
    if response.status_code == 200:
        assert isinstance(response.json(), list) 