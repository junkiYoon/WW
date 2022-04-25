from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from src.core.models.user import User_tbl

from src.utils.security import get_password_hash, verify_password, create_access_token


async def is_email(session: Session, email: str):
    user = session.query(User_tbl).filter(User_tbl.email == email).scalar()
    return {
        "is_email": user
    }


async def is_nickname(session: Session, nickname: str):
    user = session.query(User_tbl).filter(User_tbl.nickname == nickname).scalar()
    return {
        "is_nickname": user
    }


def create_user(session: Session, email: str, password: str, nickname: str):
    session.add(
        User_tbl(
            email=email,
            password=get_password_hash(password),
            nickname=nickname
        )
    )

    return {
        "message": "success"
    }


def login(session: Session, email: str, password: str):
    user = session.query(User_tbl.id, User_tbl.password).filter(User_tbl.email == email)

    if not user.scalar():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email does not exist")

    user = user.first()
    if not verify_password(plain_password=password, hashed_password=user["password"]):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Wrong password")

    return {
        "access_token": create_access_token(user_id=user["id"])
    }
