import json
from unittest.mock import Mock
import pytest
from app.sqs_publisher import SqsPublisher


def test_publish_sends_versioned_event():
    client = Mock()
    event_id = SqsPublisher(client, "https://sqs.example/queue").publish("ExecutionCompleted", "os-1", {"ok": True})
    args = client.send_message.call_args.kwargs
    event = json.loads(args["MessageBody"])
    assert event["event_id"] == event_id
    assert event["schema_version"] == 1
    assert event["order_id"] == "os-1"


def test_publish_requires_identifiers():
    with pytest.raises(ValueError):
        SqsPublisher(Mock(), "queue").publish("", "os-1", {})
