import logging

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status
from opentelemetry import trace
from opentelemetry.propagate import inject
from pydantic import BaseModel, validator

from api_gateway.auth import get_current_user_id
from api_gateway.config import ORDER_SERVICE_URL
from api_gateway.database import delete_order_record, fetch_orders_for_user

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)
router = APIRouter(prefix="/orders", tags=["orders"])


class CreateOrderRequest(BaseModel):
    items: list[dict]
    amount: float

    @validator("amount")
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("amount must be greater than zero")
        return v


@router.get("/")
async def list_orders(current_user_id: str = Depends(get_current_user_id)):
    rows = await fetch_orders_for_user(current_user_id)
    return [dict(r) for r in rows]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(
    body: CreateOrderRequest,
    current_user_id: str = Depends(get_current_user_id),
):
    with tracer.start_as_current_span("api-gateway.create_order") as span:
        span.set_attribute("order.user_id", current_user_id)
        span.set_attribute("order.item_count", len(body.items))

        logger.info("Creating order", extra={
            "event": "order.create",
            "user_id": current_user_id,
            "item_count": len(body.items),
        })

        headers: dict[str, str] = {}
        inject(headers)

        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                resp = await client.post(
                    f"{ORDER_SERVICE_URL}/internal/orders",
                    json={"user_id": current_user_id, "items": body.items, "amount": body.amount},
                    headers=headers,
                )
        except httpx.TimeoutException as e:
            logger.error(f"Order service timed out: {e}")
            raise HTTPException(status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail="Order service unavailable")

        if resp.status_code != 201:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)

        return resp.json()


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: str,
    current_user_id: str = Depends(get_current_user_id),
):
    await delete_order_record(order_id, current_user_id)
