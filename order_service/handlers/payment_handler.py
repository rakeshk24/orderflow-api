import logging

from opentelemetry import trace

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


async def process_payment(order_data: dict) -> dict:
    order_id = order_data.get("order_id", "unknown")
    with tracer.start_as_current_span(f"order-service.process_payment/{order_id}") as span:
        span.set_attribute("order.id", order_id)
        span.set_attribute("order.amount", order_data.get("amount", 0))

        try:
            logger.info("Processing payment", extra={
                "event": "payment.process",
                "order_id": order_id,
                "amount": order_data.get("amount"),
            })
            if not order_data.get("amount"):
                raise ValueError("Missing payment amount")
            return {"status": "charged", "amount": order_data.get("amount")}
        except Exception as e:
            logger.error(f"Payment failed: {e}")
            return {"status": "failed", "error": str(e)}
