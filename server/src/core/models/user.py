from sqlalchemy import Column, INTEGER, VARCHAR

from src.core.models import Base


class User_tbl(Base):
    __tablename__ = "user_tbl"

    id = Column(INTEGER, primary_key=True, autoincrement=True)
    email = Column(VARCHAR(45), nullable=False)
    password = Column(VARCHAR(225), nullable=False)
    nickname = Column(VARCHAR(10), nullable=False)
