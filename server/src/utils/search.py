from sqlalchemy import func, or_
from sqlalchemy.orm import Session

from src.core.models.content import Content_tbl
from src.core.models.user import User_tbl
from src.core.models.review import Review_tbl
from src.core.models.availability_tbl import Availability_tbl

from src.utils import get_genre


def get_search_result(session: Session, title: str, platform: list, category: str, genre: list):
    sq = session.query(func.max(Review_tbl.created_at)).group_by(Review_tbl.content_id).subquery()
    gen = get_genre(session=session)
    query = session.query(
        Content_tbl.id,
        Content_tbl.poster_url,
        Content_tbl.title,
        gen.c.genre,
        Content_tbl.synopsis,
        User_tbl.nickname,
        Review_tbl.comment
    )\
        .join(gen, Content_tbl.id == gen.c.content_id)\
        .join(Review_tbl, Content_tbl.id == Review_tbl.content_id)\
        .join(User_tbl, Review_tbl.user_id == User_tbl.id)\
        .filter(Content_tbl.title.like(f"%{title}%"))\
        .filter(Review_tbl.created_at.in_(sq))\
        .group_by(
        Content_tbl.id,
        Content_tbl.poster_url,
        Content_tbl.title,
        Content_tbl.synopsis,
        User_tbl.nickname,
        Review_tbl.comment
    )

    if platform:
        query = query.join(Availability_tbl, Content_tbl.id == Availability_tbl.content_id)\
            .filter(Availability_tbl.platform_id.in_(platform))
    if category:
        query = query.filter(Content_tbl.category.in_(category))
    if genre:
        query = query.filter(or_(*[gen.c.genre.like(f"%{g}%") for g in genre]))

    contents = query.all()

    return [{
        "id": id,
        "poster_url": poster_url,
        "title": title_,
        "genre": genre_,
        "synopsis": synopsis,
        "comment": {
            "nickname": nickname,
            "comment": comment
        },
        "word_cloud": f"/Users/junkiyoon/Documents/Git/WW/util/wcs/{id}.png"
    } for id, poster_url, title_, genre_, synopsis,  nickname, comment in contents]
