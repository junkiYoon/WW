from sqlalchemy import Column, INTEGER, TEXT

from src.core.models import Base


class Availability_tbl(Base):
    __tablename__ = "availability_tbl"

    content_id = Column(INTEGER, primary_key=True)
    platform_id = Column(INTEGER, primary_key=True)
    url = Column(TEXT, nullable=False)
