from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_list_and_filter_labs() -> None:
    response = client.get("/api/v1/labs", params={"category": "Kubernetes"})
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_unknown_lab_returns_404() -> None:
    assert client.get("/api/v1/labs/999").status_code == 404

