from fastapi.testclient import TestClient

from shelfsight.main import app

client = TestClient(app)


def test_health_check():
    resp = client.get("/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
