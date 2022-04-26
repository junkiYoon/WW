from sqlalchemy import Column, INTEGER, VARCHAR, TEXT

from src.core.models import Base


class Content_tbl(Base):
    __tablename__ = "content_tbl"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    title = Column(VARCHAR(80), nullable=False)
    synopsis = Column(TEXT)
    poster_url = Column(TEXT, nullable=False)
    category = Column(VARCHAR(5))
