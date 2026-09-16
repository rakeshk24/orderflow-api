from fastapi import FastAPI

from shared.middleware import TracingMiddleware
from shared.telemetry import setup_telemetry
from api_gateway.routers import orders, users

setup_telemetry("api-gateway")

app = FastAPI(title="OrderFlow API Gateway")
app.add_middleware(TracingMiddleware)

app.include_router(users.router)
app.include_router(orders.router)


@app.get("/health")
async def health():
    return {"status": "ok"}
