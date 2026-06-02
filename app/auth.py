import uuid
from fastapi import Header, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.db_models import User


def generate_api_key():
    return str(uuid.uuid4())


def get_current_user(
    x_api_key: str = Header(None),
    db: Session = Depends(get_db)
):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key missing")

    user = db.query(User).filter(User.api_key == x_api_key).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid API key")

    return {
        "id": user.id,
        "name": user.name,
        "api_key": user.api_key,
        "role": user.role
    }


def is_admin(current_user: dict) -> bool:
    return current_user["role"] == "admin"