from sqlalchemy import Column, INTEGER, SMALLINT, VARCHAR, DATE

from src.core.models import Base


class Review_tbl(Base):
    __tablename__ = "review_tbl"

    user_id = Column(INTEGER, primary_key=True)
    content_id = Column(INTEGER, primary_key=True)
    rate = Column(SMALLINT, nullable=False)
    comment = Column(VARCHAR(100), nullable=False)
    created_at = Column(DATE, nullable=False)
