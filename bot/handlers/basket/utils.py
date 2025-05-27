from aiogram.types import LabeledPrice
from sqlalchemy import select
from models import Basket, Product, Order, OrderItem
from db import connection


@connection
async def get_basket_by_user_id(session, user_id: str) -> list[Basket]:
    query = select(Basket).where(Basket.user_id == user_id)
    result = await session.execute(query)
    baskets = result.scalars().all() if result else []
    return baskets


@connection
async def get_basket_item(session, user_id: str, product_id: int) -> Basket | None:
    query = select(Basket).where(
        Basket.user_id == user_id, Basket.product_id == product_id
    )
    result = await session.execute(query)
    basket_item = result.scalar_one_or_none()
    return basket_item


@connection
async def add_to_basket(
    session, user_id: str, product_id: int, quantity: int = 1
) -> Basket:
    basket_item = await get_basket_item(user_id, product_id)
    if basket_item:
        basket_item.quantity += quantity
        await session.commit()
        return basket_item

    new_basket_item = Basket(user_id=user_id, product_id=product_id, quantity=quantity)
    session.add(new_basket_item)
    await session.commit()
    return new_basket_item


@connection
async def remove_from_basket(
    session, user_id: str, product_id: int, quantity: int
) -> (bool, str):
    query = select(Basket).where(
        Basket.user_id == user_id, Basket.product_id == product_id
    )
    result = await session.execute(query)
    basket_item = result.scalar_one_or_none()
    if basket_item is None:
        return False, "Товар не найден в корзине."
    new_quantity = max(basket_item.quantity - quantity, 0)
    if new_quantity == 0:
        await session.delete(basket_item)
        await session.commit()
        return True, "Товар успешно удален из корзины."
    else:
        basket_item.quantity = new_quantity
        await session.commit()
        return True, f"Сейчас в корзине осталось {new_quantity} шт. товара."


@connection
async def clear_basket(session, user_id: str) -> None:
    query = select(Basket).where(Basket.user_id == user_id)
    result = await session.execute(query)
    basket_items = result.scalars().all()

    for item in basket_items:
        await session.delete(item)

    await session.commit()


@connection
async def get_basket(session, user_id: str) -> list[tuple[Basket, Product]]:
    query = (
        select(Basket, Product)
        .join(Product, Basket.product_id == Product.id)
        .where(Basket.user_id == user_id)
    )
    result = await session.execute(query)
    return result.all()


@connection
async def save_order(session, user_id: str, address: str) -> None:
    basket_items = await get_basket(user_id)
    if not basket_items:
        return
    new_order = Order(user_id=user_id, address=address)
    session.add(new_order)
    await session.flush()

    for basket_item, product in basket_items:
        session.add(
            OrderItem(
                order_id=new_order.id,
                product_id=product.id,
                quantity=basket_item.quantity,
                price=product.price,
            )
        )

    await session.commit()
    return new_order


async def get_labeled_prices(callback) -> list[LabeledPrice]:
    return [
        LabeledPrice(
            label="Оплата заказа",
            amount=int(
                100
                * sum(
                    product.price * basket_item.quantity
                    for basket_item, product in await get_basket(
                        str(callback.from_user.id)
                    )
                )
            ),
        )
    ]
