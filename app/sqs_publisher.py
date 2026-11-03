"""SQS event publisher. Caller must ensure durable outbox for production."""
import json
import os
from uuid import uuid4


class SqsPublisher:
    def __init__(self, client, queue_url: str):
        self.client = client
        self.queue_url = queue_url

    @classmethod
    def from_environment(cls):
        import boto3
        return cls(boto3.client("sqs"), os.environ["EXECUTION_QUEUE_URL"])

    def publish(self, event_type: str, order_id: str, payload: dict) -> str:
        if not event_type or not order_id:
            raise ValueError("event_type and order_id are required")
        event_id = str(uuid4())
        body = {
            "schema_version": 1,
            "event_id": event_id,
            "event_type": event_type,
            "order_id": order_id,
            "payload": payload,
        }
        self.client.send_message(QueueUrl=self.queue_url, MessageBody=json.dumps(body))
        return event_id
