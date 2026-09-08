from fastapi.testclient import TestClient

from app.main import app


def test_info() -> None:
    with TestClient(app) as client:
        response = client.get("/api/v1/info")
    assert response.status_code == 200
    assert response.json()["name"] == "api-gateway"

