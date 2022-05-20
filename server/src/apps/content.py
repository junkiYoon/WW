from fastapi import APIRouter, status, Depends

from src import Settings, get_settings

from src.core.models import session_scope
from src.core.models.user import User_tbl

from src.utils.security import get_current_user
from src.utils.content import (
    get_content_recommendation,
    post_like,
    delete_like,
    get_like_content,
    post_pin,
    delete_pin,
    get_pin_content,
    get_content_detail
)


router = APIRouter()


@router.get("/recommend", status_code=status.HTTP_200_OK)
def recommend_content(user: User_tbl = Depends(get_current_user), settings: Settings = Depends(get_settings)):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = get_content_recommendation(session=session, user_id=user.id)

        return response


@router.post("/like", status_code=status.HTTP_201_CREATED)
async def like_content(
        content_id: int,
        user: User_tbl = Depends(get_current_user),
        settings: Settings = Depends(get_settings)
):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = post_like(session=session, user_id=user.id, content_id=content_id)

        return response


@router.delete("/like", status_code=status.HTTP_204_NO_CONTENT)
async def unlike_content(
        content_id: int,
        user: User_tbl = Depends(get_current_user),
        settings: Settings = Depends(get_settings)
):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = delete_like(session=session, user_id=user.id, content_id=content_id)

        return response


@router.get("/like", status_code=status.HTTP_200_OK)
def user_like_contents(
        page: int,
        user: User_tbl = Depends(get_current_user),
        settings: Settings = Depends(get_settings)
):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = get_like_content(session=session, user_id=user.id, page=page)

        return response


@router.post("/pin", status_code=status.HTTP_201_CREATED)
async def pin_content(
        content_id: int,
        user: User_tbl = Depends(get_current_user),
        settings: Settings = Depends(get_settings)
):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = post_pin(session=session, user_id=user.id, content_id=content_id)

        return response


@router.delete("/pin", status_code=status.HTTP_204_NO_CONTENT)
async def pin_content(
        content_id: int,
        user: User_tbl = Depends(get_current_user),
        settings: Settings = Depends(get_settings)
):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = delete_pin(session=session, user_id=user.id, content_id=content_id)

        return response


@router.get("/pin", status_code=status.HTTP_200_OK)
def user_pin_contents(
        page: int,
        user: User_tbl = Depends(get_current_user),
        settings: Settings = Depends(get_settings)
):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = get_pin_content(session=session, user_id=user.id, page=page)

        return response


@router.get("/detail", status_code=status.HTTP_200_OK)
def content_detail(
        content_id: int,
        user: User_tbl = Depends(get_current_user),
        settings: Settings = Depends(get_settings)
):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = get_content_detail(session=session, user_id=user.id, content_id=content_id)

        return response
