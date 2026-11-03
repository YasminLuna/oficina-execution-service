from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Oficina Execution Service", version="0.1.0")


class State(str, Enum):
    QUEUED = "QUEUED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class WorkInput(BaseModel):
    order_id: str = Field(min_length=1)


class Diagnosis(BaseModel):
    description: str = Field(min_length=1)


class WorkItem(BaseModel):
    order_id: str
    state: State = State.QUEUED
    diagnosis: str | None = None


# Development-only store; replace with DynamoDB before deployment.
items: dict[str, WorkItem] = {}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/work-items", response_model=WorkItem, status_code=201)
def enqueue(data: WorkInput):
    if data.order_id in items:
        raise HTTPException(409, "Already queued")
    item = WorkItem(order_id=data.order_id)
    items[data.order_id] = item
    return item


@app.get("/work-items/{order_id}", response_model=WorkItem)
def get_item(order_id: str):
    if order_id not in items:
        raise HTTPException(404, "Work item not found")
    return items[order_id]


@app.post("/work-items/{order_id}/start", response_model=WorkItem)
def start(order_id: str):
    item = get_item(order_id)
    if item.state != State.QUEUED:
        raise HTTPException(409, "Not queued")
    item = item.model_copy(update={"state": State.IN_PROGRESS})
    items[order_id] = item
    return item


@app.post("/work-items/{order_id}/complete", response_model=WorkItem)
def complete(order_id: str, data: Diagnosis):
    item = get_item(order_id)
    if item.state != State.IN_PROGRESS or not data.description.strip():
        raise HTTPException(409, "In-progress item and nonblank diagnosis required")
    item = item.model_copy(update={"state": State.COMPLETED, "diagnosis": data.description.strip()})
    items[order_id] = item
    return item


@app.post("/work-items/{order_id}/cancel", response_model=WorkItem)
def cancel(order_id: str):
    item = get_item(order_id)
    if item.state != State.QUEUED:
        raise HTTPException(409, "Only queued items can be cancelled")
    item = item.model_copy(update={"state": State.CANCELLED})
    items[order_id] = item
    return item
