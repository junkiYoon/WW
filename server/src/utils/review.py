from fastapi import HTTPException, status

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.core.models.review import Review_tbl
from src.core.models.user import User_tbl


async def post_review(session: Session, user_id: int, content_id: int, rate: int, comment: str):
    if session.query(Review_tbl).filter(and_(Review_tbl.user_id==user_id, Review_tbl.content_id==content_id)).scalar():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="review already exist")

    session.add(
        Review_tbl(
            user_id=user_id,
            content_id=content_id,
            rate=rate,
            comment=comment
        )
    )

    return {
        "message": "success"
    }


def get_reviews(session: Session, content_id: int, page: int):
    limit = 10
    offset = (page - 1) * limit

    reviews = session.query(
        User_tbl.nickname,
        Review_tbl.created_at,
        Review_tbl.rate,
        Review_tbl.comment
    )\
        .join(Review_tbl, User_tbl.id == Review_tbl.user_id)\
        .filter(Review_tbl.content_id == content_id)\
        .order_by(Review_tbl.created_at.desc())\
        .limit(limit).offset(offset).all()

    return [{
        "nickname": nickname,
        "created_at": created_at,
        "rate": rate,
        "comment": comment
    } for nickname, created_at, rate, comment in reviews]
