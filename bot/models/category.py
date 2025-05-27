from sqlalchemy import Column, String, Integer
from .base import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    parent_id = Column(Integer, nullable=True, default=None)
