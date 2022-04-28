from sqlalchemy import Column, INTEGER, TIMESTAMP

from src.core.models import Base


class Pin_tbl(Base):
    __tablename__ = "pin_tbl"

    user_id = Column(INTEGER, primary_key=True)
    content_id = Column(INTEGER, primary_key=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default="CURRENT_TIMESTAMP")
