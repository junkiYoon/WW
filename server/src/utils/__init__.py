from sqlalchemy import literal_column
from sqlalchemy.orm import Session

from src.core.models.genre import Genre_tbl
from src.core.models.availability_tbl import Availability_tbl
from src.core.models.platform import Platform_tbl


def get_genre(session: Session):
    return session.query(
        Genre_tbl.content_id,
        literal_column(
            "GROUP_CONCAT(genre_tbl.genre ORDER BY genre_tbl.genre SEPARATOR ', ') AS genre"
        )
    ).group_by(Genre_tbl.content_id).subquery()


def get_platforms(session: Session):
    return session.query(
        Availability_tbl.content_id,
        "GROUP_CONCAT("
        "CONCAT(platform_tbl.name, ';', platform_tbl.logo_url, ';', availability_tbl.url) "
        "ORDER BY platform_tbl.id "
        "SEPARATOR '|'"
        ") AS platforms"
    ).join(Platform_tbl, Availability_tbl.platform_id == Platform_tbl.id)\
        .group_by(Availability_tbl.content_id).subquery()
