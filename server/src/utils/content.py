from fastapi import HTTPException, status

from sqlalchemy import func, and_
from sqlalchemy.orm import Session

import pandas as pd

from sklearn.metrics.pairwise import cosine_similarity

from src.core.models.like import Like_tbl
from src.core.models.content import Content_tbl
from src.core.models.review import Review_tbl
from src.core.models.user import User_tbl
from src.core.models.pin import Pin_tbl

from src.utils import get_genre, get_platforms



def get_content_recommendation(session: Session, user_id: int):
    like_ids = session.query(Like_tbl.content_id).filter(Like_tbl.user_id == user_id).all()

    sq = session.query(func.max(Review_tbl.created_at)).group_by(Review_tbl.content_id).subquery()
    genre = get_genre(session=session)
    query = session.query(
        Content_tbl.id,
        Content_tbl.poster_url,
        Content_tbl.title,
        genre.c.genre,
        Content_tbl.synopsis,
        User_tbl.nickname,
        Review_tbl.comment
    )\
        .join(genre, Content_tbl.id == genre.c.content_id)\
        .join(Review_tbl, Content_tbl.id == Review_tbl.content_id)\
        .join(User_tbl, Review_tbl.user_id == User_tbl.id) \
        .filter(Review_tbl.created_at.in_(sq))\
        .group_by(
        Content_tbl.id,
        Content_tbl.poster_url,
        Content_tbl.title,
        Content_tbl.synopsis,
        User_tbl.nickname,
        Review_tbl.comment
    )

    if like_ids:
        rate_df = pd.read_sql_query("SELECT user_id, content_id, rate "
                                    "FROM content_tbl "
                                    "LEFT OUTER JOIN review_tbl ON content_tbl.id = review_tbl.content_id;", session.bind)
        movie_user_rating = rate_df.pivot_table("rate", index="content_id", columns="user_id").fillna(0)
        item_based_collaboration = cosine_similarity(movie_user_rating)
        preference = pd.DataFrame(item_based_collaboration, index=movie_user_rating.index, columns=movie_user_rating.index)

        recommend_ids = preference[like_ids[-1]["content_id"]].dropna()
        for id in like_ids[:-1]:
            recommend_ids = recommend_ids.append(preference[id["content_id"]]).dropna()
        recommend_ids = set(recommend_ids.sort_values(ascending=False).index) - set(id["content_id"] for id in like_ids)

        contents = query.filter(Content_tbl.id.in_(recommend_ids)).all()
    else:
        contents = query.order_by(func.rand(Content_tbl.id)).limit(10).all()

    return [{
        "id": id,
        "poster_url": poster_url,
        "title": title,
        "genre": genre,
        "synopsis": synopsis,
        "comment": {
            "nickname": nickname,
            "comment": comment
        },
        "word_cloud": f"/Users/junkiyoon/Documents/Git/WW/util/wcs/{id}.png"
    } for id, poster_url, title, genre, synopsis, nickname, comment in contents]


async def post_like(session: Session, user_id: int, content_id: int):
    if not session.query(Content_tbl).filter(Content_tbl.id == Content_tbl).scalar():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find such content")

    session.add(Like_tbl(user_id=user_id, content_id=content_id))

    return {
        "message": "success"
    }


async def delete_like(session: Session, user_id: int, content_id: int):
    if not session.query(Content_tbl).filter(Content_tbl.id == Content_tbl).scalar():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find such content")

    session.delete(Like_tbl).filter(and_(Like_tbl.user_id == user_id, Like_tbl.content_id == content_id))

    return {
        "message": "success"
    }


def get_like_content(session: Session, user_id: int, page: int):
    limit = 20
    offset = (page - 1) * limit

    genre = get_genre(session=session)
    contents = session.query(
        Content_tbl.id,
        Content_tbl.poster_url,
        Content_tbl.title,
        genre.c.genre
    )\
        .join(Like_tbl, Content_tbl.id == Like_tbl.content_id) \
        .join(genre, Content_tbl.id == genre.c.content_id)\
        .filter(Like_tbl.user_id == user_id)\
        .order_by(Like_tbl.created_at)\
        .limit(limit).offset(offset).all()

    return [{
        "id": id,
        "poster_url": poster_url,
        "title": title,
        "genre": genre
    } for id, poster_url, title, genre in contents]


async def post_pin(session: Session, user_id: int, content_id: int):
    if not session.query(Content_tbl).filter(Content_tbl.id == Content_tbl).scalar():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find such content")

    session.add(Pin_tbl(user_id=user_id, content_id=content_id))

    return {
        "message": "success"
    }


async def delete_pin(session: Session, user_id: int, content_id: int):
    if not session.query(Content_tbl).filter(Content_tbl.id == Content_tbl).scalar():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Could not find such content")

    session.delete(Pin_tbl).filter(and_(Pin_tbl.user_id == user_id, Pin_tbl.content_id == content_id))

    return {
        "message": "success"
    }


def get_pin_content(session: Session, user_id: int, page: int):
    limit = 20
    offset = (page - 1) * limit

    genre = get_genre(session=session)
    contents = session.query(
        Content_tbl.id,
        Content_tbl.poster_url,
        Content_tbl.title,
        genre.c.genre
    )\
        .join(Pin_tbl, Content_tbl.id == Pin_tbl.content_id)\
        .join(genre, Content_tbl.id == genre.c.content_id)\
        .filter(Pin_tbl.user_id == user_id)\
        .order_by(Pin_tbl.created_at)\
        .limit(limit).offset(offset).all()

    return [{
        "id": id,
        "poster_url": poster_url,
        "title": title,
        "genre": genre
    } for id, poster_url, title, genre in contents]


def get_content_detail(session: Session, user_id: int, content_id: int):
    genre = get_genre(session=session)
    platforms = get_platforms(session=session)
    content = session.query(
        Content_tbl.title,
        Content_tbl.poster_url,
        func.IF(func.isnull(Pin_tbl.user_id) == 1, False, True).label("is_pin"),
        func.IF(func.isnull(Like_tbl.user_id) == 1, False, True).label("is_like"),
        genre.c.genre,
        Content_tbl.synopsis,
        platforms.c.platforms
    )\
        .join(genre, Content_tbl.id == genre.c.content_id)\
        .outerjoin(Pin_tbl, and_(Content_tbl.id == Pin_tbl.content_id, Pin_tbl.user_id == user_id))\
        .outerjoin(Like_tbl, and_(Content_tbl.id == Like_tbl.content_id, Like_tbl.user_id == user_id))\
        .join(platforms, Content_tbl.id == platforms.c.content_id)\
        .filter(Content_tbl.id == content_id)\
        .first()

    return {
        "title": content["title"],
        "poster_url": content["poster_url"],
        "is_pin": content["is_pin"],
        "is_like": content["is_like"],
        "genre": content["genre"],
        "synopsis": content["synopsis"],
        "platforms": [{
            "name": name,
            "logo": logo,
            "url": url
        } for name, logo, url in map(lambda p: p.split(";"), content["platforms"].split("|"))],
        "word_cloud": f"/Users/junkiyoon/Documents/Git/WW/util/wcs/{content_id}.png"
    }
