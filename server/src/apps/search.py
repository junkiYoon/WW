from fastapi import APIRouter, status, Query, Depends

from typing import Optional, List

from src import Settings, get_settings

from src.core.models import session_scope

from src.utils.search import get_search_result


router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
def search_content(
        title: str,
        platform: Optional[List[int]] = Query(None),
        category: Optional[str] = Query(None),
        genre: Optional[List[str]] = Query(None),
        settings: Settings = Depends(get_settings)
):
    with session_scope(settings.MYSQL_DB_URL) as session:
        response = get_search_result(session=session, title=title, platform=platform, category=category, genre=genre)

        return response
