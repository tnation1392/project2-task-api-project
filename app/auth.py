from fastapi import Depends, HTTPException, Security, status
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session
from app.db import get_db
from app.db_models import User
import secrets

API_KEY_HEADER_NAME = "X-API-Key"

api_key_header = APIKeyHeader(
    name=API_KEY_HEADER_NAME,
    scheme_name="ApiKeyAuth",
    description="API key required in the X-API-Key header",
    auto_error=False,
)


def generate_api_key() -> str:
    return secrets.token_hex(16)


def get_current_user(
    api_key: str | None = Security(api_key_header),
    db: Session = Depends(get_db),
):
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API key",
        )

    user = db.query(User).filter(User.api_key == api_key).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    return {
        "id": user.id,
        "name": user.name,
        "api_key": user.api_key,
        "role": user.role,
    }


def is_admin(current_user: dict = Depends(get_current_user)):
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )

    return current_user