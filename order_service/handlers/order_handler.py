import logging
import uuid

from opentelemetry import trace

from order_service.handlers.payment_handler import process_payment

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


async def create_order(order_data: dict, incoming_headers: dict) -> dict:
    with tracer.start_as_current_span("order-service.create_order") as span:
        order_id = str(uuid.uuid4())
        span.set_attribute("order.id", order_id)
        span.set_attribute("order.user_id", order_data.get("user_id", ""))
        span.set_attribute("order.amount", order_data.get("amount", 0))

        logger.info(
            f"Creating order {order_id} for user {order_data.get('user_id')} "
            f"email {order_data.get('user_email')} amount {order_data.get('amount')}"
        )

        payment_result = await process_payment({**order_data, "order_id": order_id})

        return {"order_id": order_id, "status": "created", "payment": payment_result}
