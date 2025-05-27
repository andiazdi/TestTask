from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from .base import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(length=255), nullable=False)
    address = Column(String, nullable=False)

    items = relationship("OrderItem", back_populates="order", cascade="all, delete")
