from fastapi import APIRouter, status, Depends

from src import Settings, get_settings

from src.core.models import session_scope
from src.core.models.user import User_tbl

from src.core.schemas.review import Create_review

from src.utils.security import get_current_user
from src.utils.review import post_review, get_reviews


router = APIRouter()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_review(
        content_id: int,
        body: Create_review,
        user: User_tbl = Depends(get_current_user),
        settings: Settings = Depends(get_settings)
):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = await post_review(
            session=session,
            user_id=user.id,
            content_id=content_id,
            rate=body.rate,
            comment=body.comment
        )

        return response


@router.get("", status_code=status.HTTP_200_OK)
def get_review(
        content_id: int,
        page: int,
        user: User_tbl = Depends(get_current_user),
        settings: Settings = Depends(get_settings)
):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = get_reviews(session=session, content_id=content_id, page=page)

        return response
