import logging
import random

from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, PreCheckoutQuery, Message
from .markups import BasketMarkup
from .utils import (
    add_to_basket,
    get_basket_item,
    get_basket,
    remove_from_basket,
    clear_basket,
    get_labeled_prices,
    save_order,
)
from handlers.catalog.markups import CatalogMarkup
from .states import BasketState
from config import PAYMENT_TOKEN

router = Router()


@router.message(F.text == "Корзина 🛒")
async def show_basket(message):
    user_id = str(message.from_user.id)
    basket = await get_basket(user_id)
    if not basket:
        await message.answer(
            "🛒 <b>Ваша корзина пуста.</b>\n\nДобавьте товары, чтобы начать покупки!",
            reply_markup=await CatalogMarkup.get_categories_markup(),
        )
        return
    text = "🛒 <b>Ваша корзина:</b>\n\n"
    total = 0

    for basket_item, product in basket:
        subtotal = product.price * basket_item.quantity
        total += subtotal
        text += (
            f"📦 <b>{product.title}</b>\n"
            f"    Кол-во: <b>{basket_item.quantity}</b>\n"
            f"    Цена за шт.: <b>{product.price}₽</b>\n"
            f"    Всего: <b>{subtotal}₽</b>\n\n"
        )

    text += f"💰 <b>Итого: {total}₽</b>\n\nНажмите на товар, чтобы уменьшить его количество в корзине:"
    await message.answer(
        text,
        reply_markup=await BasketMarkup.get_basket_markup(user_id, 1),
    )


@router.callback_query(F.data.startswith("add_to_cart_"))
async def add_to_cart_handler(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split("_")[3])
    product = await get_basket_item(str(callback.from_user.id), product_id)
    quantity_info = ""
    if product:
        quantity_info = f" (сейчас в корзине: {product.quantity}"
    message = await callback.message.answer(
        f"Введите количество товара, которое вы хотите добавить в корзину{quantity_info}:",
        reply_markup=BasketMarkup.get_cancel_button(),
    )
    await state.set_state(BasketState.add_to_basket)
    await state.update_data(product_id=product_id, message=message)


@router.message(BasketState.add_to_basket)
async def add_to_cart_quantity_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    product_id = data.get("product_id")
    quantity = message.text

    if not quantity.isdigit() or int(quantity) <= 0:
        await message.answer("Пожалуйста, введите корректное количество товара.")
        return

    quantity = int(quantity)
    await add_to_basket(
        user_id=str(message.from_user.id), product_id=product_id, quantity=quantity
    )
    if data.get("message"):
        await data["message"].delete()
    await message.answer(
        f"Товар успешно добавлен в корзину. Количество: {quantity}",
        reply_markup=await CatalogMarkup.get_categories_markup(),
    )
    await state.clear()


@router.callback_query(F.data == "cancel_basket_action")
async def cancel_basket_action_handler(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()


@router.callback_query(F.data.startswith("remove_basket_page_"))
async def remove_basket_page_handler(callback: CallbackQuery):
    page = int(callback.data.split("_")[3])
    markup = await BasketMarkup.get_basket_markup(str(callback.from_user.id), page)
    if len(markup.inline_keyboard) > 1:
        await callback.message.edit_text("🛒 <b>Ваша корзина:</b>", reply_markup=markup)
    else:
        await callback.message.edit_text(
            "Корзина пуста.", reply_markup=await CatalogMarkup.get_categories_markup()
        )


@router.callback_query(F.data.startswith("remove_basket_item_"))
async def remove_from_basket_handler(callback: CallbackQuery, state: FSMContext):
    product_id = int(callback.data.split("_")[3])
    user_id = callback.from_user.id

    await callback.message.answer(
        "Введите количество товара, которое вы хотите удалить из корзины:",
        reply_markup=BasketMarkup.get_cancel_button(),
    )
    await state.set_state(BasketState.remove_from_basket)
    await state.update_data(product_id=product_id, user_id=str(user_id))


@router.message(BasketState.remove_from_basket)
async def remove_from_basket_quantity_handler(message: Message, state: FSMContext):
    data = await state.get_data()
    product_id = data.get("product_id")
    user_id = data.get("user_id")
    quantity = message.text
    if not quantity.isdigit() or int(quantity) <= 0:
        await message.answer("Пожалуйста, введите корректное количество товара.")
        return
    quantity = int(quantity)
    status, info = await remove_from_basket(user_id, product_id, quantity)
    if status:
        await message.answer(
            f"Товар успешно удален из корзины. {info}",
            reply_markup=await BasketMarkup.get_basket_markup(user_id, 1),
        )
    else:
        await message.answer(f"Не удалось удалить товар из корзины. {info}")

    await state.clear()


@router.callback_query(F.data == "basket_pay")
async def basket_pay_handler(callback: CallbackQuery, state: FSMContext):
    logging.info(f"User {callback.from_user.id} initiated payment from basket.")
    await state.set_state(BasketState.pass_address)
    await callback.message.delete()
    message = await callback.message.answer(
        "📦 Пожалуйста, введите 🏠 адрес доставки для оформления заказа:",
        reply_markup=BasketMarkup.get_cancel_button(),
    )
    await state.update_data(message=message)


@router.message(BasketState.pass_address)
async def pass_address_handler(message: Message, state: FSMContext):
    logging.info(
        f"User {message.from_user.id} provided address: {message.text.strip()}"
    )
    address = message.text.strip()
    data = await state.get_data()
    if data.get("message"):
        await data["message"].delete()
    await state.update_data(address=address)
    await message.answer(
        f"Подтвердите адрес доставки 🏠:\n\n <b>{address}</b>\n\n",
        reply_markup=BasketMarkup.get_confirmation_address_markup(),
    )


@router.callback_query(F.data == "confirm_address")
async def confirm_address_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    address = data.get("address")

    await callback.message.delete()
    if not address:
        await callback.message.answer(
            "Адрес не указан. Пожалуйста, введите адрес доставки."
        )
        return
    prices = await get_labeled_prices(callback)
    await state.clear()
    await state.update_data(address=address)
    try:
        logging.info(
            f"User {callback.from_user.id} is paying for order with address: {address}"
        )
        await callback.message.answer_invoice(
            title="Оплата заказа",
            description=f"Доставка по адресу: {address}",
            payload=f"order_payload_{random.randint(1, 100)}",
            provider_token=PAYMENT_TOKEN,
            currency="RUB",
            prices=prices,
            start_parameter="order-start",
        )
    except TelegramBadRequest as e:
        if "CURRENCY_TOTAL_AMOUNT_INVALID" in str(e):
            logging.error(
                f"Total amount exceeds limit for user {callback.from_user.id}: {e}"
            )
            await callback.message.answer(
                "Ошибка: слишком большая сумма заказа. Проверьте правильность указания цены."
            )
        else:
            logging.error(
                f"Error sending invoice for user {callback.from_user.id}: {e}"
            )
            await callback.message.answer(
                f"Ошибка при отправке счета. Попробуйте позже."
            )


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)
    logging.info(
        f"Pre-checkout query received from user {pre_checkout_query.from_user.id}."
    )


@router.message(F.content_type == ContentType.SUCCESSFUL_PAYMENT)
async def successful_payment(message: Message, state: FSMContext):
    total_amount = message.successful_payment.total_amount / 100
    user_id = str(message.from_user.id)
    logging.info(f"User {user_id} successfully paid {total_amount} RUB for order.")
    await message.answer(
        f"Оплата прошла успешно ✅!\nСумма: <b>{total_amount:.2f}</b> ₽\n\nСпасибо за покупку ❤️!"
    )
    await save_order(
        user_id=user_id,
        address=await state.get_value("address", "Не указан"),
    )
    logging.info(
        f'Order saved for user {user_id} with address: {await state.get_value("address", "Не указан")}'
    )
    await clear_basket(user_id)
    logging.debug(f"User {user_id}'s basket cleared after finishing payment.")
