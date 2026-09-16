from fastapi import FastAPI, Request, status

from shared.logging_config import setup_logging
from shared.middleware import TracingMiddleware
from shared.telemetry import setup_telemetry
from order_service.handlers.order_handler import create_order

setup_telemetry("order-service")
setup_logging()

app = FastAPI(title="OrderFlow Order Service")
app.add_middleware(TracingMiddleware)


@app.post("/internal/orders", status_code=status.HTTP_201_CREATED)
async def internal_create_order(request: Request, body: dict):
    result = await create_order(body, dict(request.headers))
    return result


@app.get("/health")
async def health():
    return {"status": "ok"}
