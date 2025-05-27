from sqlalchemy import Column, ForeignKey, Integer, String
from .base import Base


class Basket(Base):
    __tablename__ = "basket"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(length=255), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, default=1)
