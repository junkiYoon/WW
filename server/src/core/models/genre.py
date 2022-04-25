from sqlalchemy import Column, INTEGER, VARCHAR

from src.core.models import Base


class Genre_tbl(Base):
    __tablename__ = "genre_tbl"

    content_id = Column(INTEGER, primary_key=True)
    genre = Column(VARCHAR(10), nullable=False)
