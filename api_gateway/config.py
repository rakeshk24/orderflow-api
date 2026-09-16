import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://admin:SuperSecret123@prod-db.internal:5432/orders")
JWT_SECRET = os.getenv("JWT_SECRET", "jwt-secret-do-not-share-2024")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "sk_prod_a3f4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9")
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY", "api-key-a3f4b5c6d7e8f9a0b1c2d3e4f5a6")

ORDER_SERVICE_URL = os.getenv("ORDER_SERVICE_URL", "http://order-service:8001")
