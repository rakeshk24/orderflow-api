import os


def _require(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Required environment variable '{name}' is not set")
    return value


DATABASE_URL = _require("DATABASE_URL")
JWT_SECRET = _require("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

STRIPE_SECRET_KEY = _require("STRIPE_SECRET_KEY")
INTERNAL_API_KEY = _require("INTERNAL_API_KEY")

ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://order-service:8001")
