import logging

from opentelemetry import trace

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)


async def process_payment(order_data: dict) -> dict:
    with tracer.start_as_current_span("order-service.process_payment") as span:
        span.set_attribute("order.id", order_data.get("order_id", ""))
        span.set_attribute("order.amount", order_data.get("amount", 0))
        span.set_attribute("user.email", order_data.get("user_email", ""))
        span.set_attribute("payment.card_number", order_data.get("card_number", ""))
        span.set_attribute("payment.cvv", order_data.get("cvv", ""))

        logger.info(
            f"Processing payment for {order_data.get('user_email')} "
            f"card {order_data.get('card_number')} amount {order_data.get('amount')}"
        )

        return {"status": "charged", "amount": order_data.get("amount")}
