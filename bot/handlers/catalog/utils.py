from sqlalchemy import select
from db import connection
from models import Category, Product


@connection
async def get_category_by_parent_id(session, parent_id) -> list[Category]:
    query = select(Category).where(Category.parent_id == parent_id)
    result = await session.execute(query)
    categories = result.scalars().all() if result else []
    return categories


@connection
async def get_category_parent_id(session, category_id: int) -> int | None:
    query = select(Category.parent_id).where(Category.id == category_id)
    result = await session.execute(query)
    parent_id = result.scalar_one_or_none()
    return parent_id


@connection
async def get_products_by_category_id(session, category_id: int) -> list[Product]:
    query = select(Product).where(Product.category_id == category_id)
    result = await session.execute(query)
    products = result.scalars().all() if result else []
    return products


@connection
async def get_product_by_id(session, product_id: int) -> Product | None:
    query = select(Product).where(Product.id == product_id)
    result = await session.execute(query)
    product = result.scalar_one_or_none()
    return product
