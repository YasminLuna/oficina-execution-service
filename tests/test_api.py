import pytest
from fastapi.testclient import TestClient
from app.main import app, items

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_items():
    items.clear()


def test_health():
    assert client.get("/health").status_code == 200


def test_happy_path():
    assert client.post("/work-items", json={"order_id": "os-1"}).status_code == 201
    assert client.post("/work-items/os-1/start").json()["state"] == "IN_PROGRESS"
    result = client.post("/work-items/os-1/complete", json={"description": "Brake pads"})
    assert result.json()["state"] == "COMPLETED"


def test_duplicate():
    client.post("/work-items", json={"order_id": "os-1"})
    assert client.post("/work-items", json={"order_id": "os-1"}).status_code == 409


def test_missing():
    assert client.get("/work-items/missing").status_code == 404


def test_cannot_complete_queued():
    client.post("/work-items", json={"order_id": "os-1"})
    assert client.post("/work-items/os-1/complete", json={"description": "Done"}).status_code == 409


def test_cancel_queued():
    client.post("/work-items", json={"order_id": "os-1"})
    assert client.post("/work-items/os-1/cancel").json()["state"] == "CANCELLED"


def test_cannot_cancel_running():
    client.post("/work-items", json={"order_id": "os-1"})
    client.post("/work-items/os-1/start")
    assert client.post("/work-items/os-1/cancel").status_code == 409


def test_cannot_start_twice():
    client.post("/work-items", json={"order_id": "os-1"})
    client.post("/work-items/os-1/start")
    assert client.post("/work-items/os-1/start").status_code == 409
