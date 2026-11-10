from unittest.mock import Mock
import pytest
from app.dynamodb_repository import DynamoExecutionRepository


def test_create_uses_conditional_write():
    table = Mock()
    result = DynamoExecutionRepository(table).create("os-1")
    assert result == {"order_id": "os-1", "state": "QUEUED"}
    assert "attribute_not_exists" in table.put_item.call_args.kwargs["ConditionExpression"]


def test_create_requires_id():
    with pytest.raises(ValueError):
        DynamoExecutionRepository(Mock()).create("")


def test_get_existing_item():
    table = Mock()
    table.get_item.return_value = {"Item": {"order_id": "os-1", "state": "QUEUED"}}
    assert DynamoExecutionRepository(table).get("os-1")["state"] == "QUEUED"


def test_get_missing_item():
    table = Mock()
    table.get_item.return_value = {}
    assert DynamoExecutionRepository(table).get("missing") is None


def test_transition_uses_compare_and_swap():
    table = Mock()
    table.update_item.return_value = {"Attributes": {"order_id": "os-1", "state": "IN_PROGRESS"}}
    result = DynamoExecutionRepository(table).transition("os-1", "QUEUED", "IN_PROGRESS")
    assert result["state"] == "IN_PROGRESS"
    assert "#state = :expected" in table.update_item.call_args.kwargs["ConditionExpression"]


def test_transition_persists_diagnosis():
    table = Mock()
    table.update_item.return_value = {"Attributes": {"order_id": "os-1", "state": "COMPLETED", "diagnosis": "Fixed"}}
    DynamoExecutionRepository(table).transition("os-1", "IN_PROGRESS", "COMPLETED", "Fixed")
    assert table.update_item.call_args.kwargs["ExpressionAttributeValues"][":diagnosis"] == "Fixed"
