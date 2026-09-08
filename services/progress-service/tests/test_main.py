from fastapi.testclient import TestClient

import app.main as main


def test_progress_round_trip(tmp_path) -> None:
    main.DATABASE_PATH = str(tmp_path / "test.db")
    with TestClient(main.app) as client:
        response = client.put("/api/v1/progress/2", json={"completed": True})
        assert response.status_code == 200
        assert response.json()["completed"] is True

        records = client.get("/api/v1/progress").json()
        assert records[0]["lab_id"] == 2
        assert records[0]["completed"] is True

