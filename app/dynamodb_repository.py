"""DynamoDB repository for execution work items.

No cross-service database access. AWS credentials are supplied by workload identity.
"""
import os
from typing import Any


class DynamoExecutionRepository:
    def __init__(self, table: Any):
        self.table = table

    @classmethod
    def from_environment(cls):
        table_name = os.environ["EXECUTION_TABLE_NAME"]
        import boto3
        return cls(boto3.resource("dynamodb").Table(table_name))

    def create(self, order_id: str) -> dict:
        if not order_id:
            raise ValueError("order_id is required")
        item = {"order_id": order_id, "state": "QUEUED"}
        self.table.put_item(
            Item=item,
            ConditionExpression="attribute_not_exists(order_id)",
        )
        return item

    def get(self, order_id: str) -> dict | None:
        response = self.table.get_item(Key={"order_id": order_id}, ConsistentRead=True)
        return response.get("Item")

    def transition(self, order_id: str, expected: str, target: str, diagnosis: str | None = None) -> dict:
        names = {"#state": "state"}
        values = {":expected": expected, ":target": target}
        expression = "SET #state = :target"
        if diagnosis is not None:
            expression += ", diagnosis = :diagnosis"
            values[":diagnosis"] = diagnosis
        response = self.table.update_item(
            Key={"order_id": order_id},
            UpdateExpression=expression,
            ConditionExpression="attribute_exists(order_id) AND #state = :expected",
            ExpressionAttributeNames=names,
            ExpressionAttributeValues=values,
            ReturnValues="ALL_NEW",
        )
        return response["Attributes"]
