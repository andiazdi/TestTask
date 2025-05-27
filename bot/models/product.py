from sqlalchemy import Column, String, Integer
from .base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, unique=True)
    description = Column(String)
    price = Column(Integer, nullable=False)
    image_path = Column(String)
    category_id = Column(Integer, nullable=False)
