from sqlalchemy import Column, INTEGER, VARCHAR

from src.core.models import Base


class Platform_tbl(Base):
    __tablename__ = "platform_tbl"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR(20), nullable=False)
    logo_url = Column(VARCHAR(255), nullable=False)
