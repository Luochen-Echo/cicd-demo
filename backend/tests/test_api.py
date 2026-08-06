from contextlib import contextmanager

from fastapi.testclient import TestClient

from app.db import get_connection
from app.main import app


@contextmanager
def _client() -> TestClient:
    with TestClient(app) as client:
        with get_connection() as conn:
            conn.execute("TRUNCATE items")
            conn.commit()
        yield client


def test_health_reports_db_ok():
    with _client() as client:
        res = client.get("/api/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok", "db": True}


def test_create_then_list_items():
    with _client() as client:
        created = client.post("/api/items", json={"name": "hello"})
        assert created.status_code == 201
        item = created.json()
        assert item["name"] == "hello"

        listed = client.get("/api/items")
        assert listed.status_code == 200
        assert listed.json() == [item]


def test_empty_list_after_truncate():
    with _client() as client:
        res = client.get("/api/items")
    assert res.status_code == 200
    assert res.json() == []
