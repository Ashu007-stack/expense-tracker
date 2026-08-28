from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate

from app.core.security import (
    hash_password,
    verify_password,
)


# ============================================================
# GET USER BY EMAIL
# ============================================================

def get_user_by_email(
    db: Session,
    email: str,
):
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


# ============================================================
# GET USER BY MOBILE NUMBER
# ============================================================

def get_user_by_mobile(
    db: Session,
    mobile_number: str,
):
    return (
        db.query(User)
        .filter(User.mobile_number == mobile_number)
        .first()
    )


# ============================================================
# CREATE USER
# ============================================================

def create_user(
    db: Session,
    user: UserCreate,
):
    db_user = User(
        full_name=user.full_name,
        email=user.email,
        mobile_number=user.mobile_number,
        hashed_password=hash_password(user.password),

        # New accounts are not verified initially
        is_mobile_verified=False,
        is_email_verified=False,

        # Account is active by default
        is_active=True,
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# ============================================================
# AUTHENTICATE USER
# ============================================================

def authenticate_user(
    db: Session,
    email: str,
    password: str,
):
    user = get_user_by_email(
        db,
        email,
    )

    if not user:
        return None

    if not verify_password(
        password,
        user.hashed_password,
    ):
        return None

    return user