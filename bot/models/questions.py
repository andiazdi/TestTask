from sqlalchemy import Column, Integer, String
from .base import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
