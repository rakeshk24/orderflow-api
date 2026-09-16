import logging

from opentelemetry import trace

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


async def process_payment(order_data: dict) -> dict:
    with tracer.start_as_current_span("order-service.process_payment") as span:
        span.set_attribute("order.id", order_data.get("order_id", ""))
        span.set_attribute("order.amount", order_data.get("amount", 0))

        logger.info("Processing payment", extra={
            "event": "payment.process",
            "order_id": order_data.get("order_id"),
            "amount": order_data.get("amount"),
        })

        return {"status": "charged", "amount": order_data.get("amount")}
