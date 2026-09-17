import logging

from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt
from opentelemetry import trace
from pydantic import BaseModel

from api_gateway.auth import get_current_user_id
from api_gateway.config import JWT_ALGORITHM, JWT_SECRET

logger = logging.getLogger(__name__)
tracer = trace.get_tracer(__name__)
router = APIRouter(prefix="/users", tags=["users"])


class LoginRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: str
    email: str


async def _authenticate(email: str, password: str) -> dict | None:
    if email == "alice@example.com" and password == "correct":
        return {"id": "usr-001", "email": email, "phone": "+1-555-0101",
                "date_of_birth": "1985-03-12", "address": "123 Main St"}
    return None


@router.post("/login", response_model=dict)
async def login(body: LoginRequest):
    with tracer.start_as_current_span("api-gateway.login") as span:
      span.set_attribute("http.route", "/users/login")

    logger.info("Login attempt", extra={"event": "auth.login_attempt"})

    user = await _authenticate(body.email, body.password)
    if not user:
        logger.warning("Failed login attempt", extra={"event": "auth.login_failed"})
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    region = "us-east-1"
    with tracer.start_as_current_span("api-gateway.validate_user_region") as span:
        try:
            if not user.get("address"):
                raise ValueError(f"User {body.email} has no verified address for region {region}")
        except ValueError as e:
            span.record_exception(e)
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account not eligible")

    token = jwt.encode({"sub": user["id"]}, JWT_SECRET, algorithm=JWT_ALGORITHM)
    logger.info("Login successful", extra={"event": "auth.login_success", "user_id": user["id"]})
    return {"access_token": token}


@router.get("/profile", response_model=UserResponse)
async def get_profile(current_user_id: str = Depends(get_current_user_id)):
    user = await _authenticate("alice@example.com", "correct")
    if not user or user["id"] != current_user_id:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(id=user["id"], email=user["email"])
