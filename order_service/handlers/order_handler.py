import logging
import uuid

from opentelemetry import trace
from opentelemetry.propagate import extract

from order_service.handlers.payment_handler import process_payment

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


async def create_order(order_data: dict, incoming_headers: dict) -> dict:
    ctx = extract(incoming_headers)

    order_id = str(uuid.uuid4())
    with tracer.start_as_current_span(f"order-service.create_order/{order_id}", context=ctx) as span:
        span.set_attribute("order.id", order_id)
        span.set_attribute("order.user_id", order_data.get("user_id", ""))
        span.set_attribute("order.amount", order_data.get("amount", 0))

        logger.info("Creating order", extra={
            "event": "order.create",
            "order_id": order_id,
            "user_id": order_data.get("user_id"),
            "item_count": len(order_data.get("items", [])),
        })

        payment_result = await process_payment({**order_data, "order_id": order_id})

        return {"order_id": order_id, "status": "created", "payment": payment_result}
