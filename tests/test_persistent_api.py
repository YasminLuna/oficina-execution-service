from unittest.mock import Mock
from fastapi.testclient import TestClient
import app.persistent_api as api


def test_dynamo_api_happy_path(monkeypatch):
    repo = Mock()
    repo.create.return_value = {"order_id": "os-1", "state": "QUEUED"}
    repo.get.return_value = {"order_id": "os-1", "state": "QUEUED"}
    repo.transition.side_effect = [
        {"order_id": "os-1", "state": "IN_PROGRESS"},
        {"order_id": "os-1", "state": "COMPLETED", "diagnosis": "Fixed"},
    ]
    monkeypatch.setattr(api, "repository", lambda: repo)
    client = TestClient(api.app)
    assert client.post("/work-items", json={"order_id": "os-1"}).status_code == 201
    assert client.get("/work-items/os-1").status_code == 200
    assert client.post("/work-items/os-1/start").json()["state"] == "IN_PROGRESS"
    assert client.post("/work-items/os-1/complete", json={"description": "Fixed"}).json()["state"] == "COMPLETED"


def test_dynamo_api_missing(monkeypatch):
    repo = Mock()
    repo.get.return_value = None
    monkeypatch.setattr(api, "repository", lambda: repo)
    assert TestClient(api.app).get("/work-items/missing").status_code == 404


def test_dynamo_api_blank_diagnosis(monkeypatch):
    repo = Mock()
    monkeypatch.setattr(api, "repository", lambda: repo)
    assert TestClient(api.app).post("/work-items/os-1/complete", json={"description": " "}).status_code == 422
    repo.transition.assert_not_called()


def test_dynamo_api_health_and_cancel(monkeypatch):
    repo = Mock()
    repo.transition.return_value = {"order_id": "os-1", "state": "CANCELLED"}
    monkeypatch.setattr(api, "repository", lambda: repo)
    client = TestClient(api.app)
    assert client.get("/health").json() == {"status": "ok"}
    assert client.post("/work-items/os-1/cancel").json()["state"] == "CANCELLED"
    repo.transition.assert_called_with("os-1", "QUEUED", "CANCELLED")


def test_dynamo_api_rejects_empty_id(monkeypatch):
    repo = Mock()
    monkeypatch.setattr(api, "repository", lambda: repo)
    client = TestClient(api.app)
    assert client.post("/work-items", json={"order_id": ""}).status_code == 422
    repo.create.assert_not_called()
