from sqlalchemy import Column, INTEGER

from src.core.models import Base


class Like_tbl(Base):
    __tablename__ = "like_tbl"

    user_id = Column(INTEGER, primary_key=True)
    content_id = Column(INTEGER, primary_key=True)
