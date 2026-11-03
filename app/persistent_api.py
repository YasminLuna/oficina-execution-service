"""Opt-in DynamoDB-backed execution API. Run: uvicorn app.persistent_api:app.

Requires EXECUTION_TABLE_NAME and AWS workload identity; no in-memory fallback.
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.dynamodb_repository import DynamoExecutionRepository

app = FastAPI(title="Oficina Execution - DynamoDB", version="0.2.0")


class OrderInput(BaseModel):
    order_id: str = Field(min_length=1)


class DiagnosisInput(BaseModel):
    description: str = Field(min_length=1)


def repository() -> DynamoExecutionRepository:
    return DynamoExecutionRepository.from_environment()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/work-items", status_code=201)
def enqueue(data: OrderInput):
    return repository().create(data.order_id)


@app.get("/work-items/{order_id}")
def get(order_id: str):
    item = repository().get(order_id)
    if item is None:
        raise HTTPException(404, "Work item not found")
    return item


@app.post("/work-items/{order_id}/start")
def start(order_id: str):
    return repository().transition(order_id, "QUEUED", "IN_PROGRESS")


@app.post("/work-items/{order_id}/complete")
def complete(order_id: str, data: DiagnosisInput):
    if not data.description.strip():
        raise HTTPException(422, "Diagnosis must not be blank")
    return repository().transition(order_id, "IN_PROGRESS", "COMPLETED", data.description.strip())


@app.post("/work-items/{order_id}/cancel")
def cancel(order_id: str):
    return repository().transition(order_id, "QUEUED", "CANCELLED")
