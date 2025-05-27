from math import ceil
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .utils import get_basket

PAGE_SIZE = 3


class BasketMarkup:
    @staticmethod
    def get_cancel_button() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="❌ Отменить",
                        callback_data=f"cancel_basket_action",
                    )
                ]
            ]
        )

    @staticmethod
    async def get_basket_markup(user_id: str, page: int = 1) -> InlineKeyboardMarkup:
        basket_items = await get_basket(user_id)

        total_pages = ceil(len(basket_items) / PAGE_SIZE)
        page = max(1, min(page, total_pages))

        start = (page - 1) * PAGE_SIZE
        end = start + PAGE_SIZE
        basket_page = basket_items[start:end]

        buttons = []
        row = []
        for i, (basket_item, product) in enumerate(basket_page, 1):
            row.append(
                InlineKeyboardButton(
                    text=f"{product.title} ({basket_item.quantity} шт.)",
                    callback_data=f"remove_basket_item_{product.id}",
                )
            )
            if i % 2 == 0 or i == len(basket_page):
                buttons.append(row)
                row = []

        pagination_buttons = []
        for p in range(1, total_pages + 1):
            text = f"{p} 🔘" if p == page else str(p)
            pagination_buttons.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=f"remove_basket_page_{p}",
                )
            )
        if pagination_buttons and len(pagination_buttons) > 1:
            buttons.append(pagination_buttons)

        if len(basket_items) > 0:
            buttons.append(
                [InlineKeyboardButton(text="Оплатить 🛒", callback_data="basket_pay")]
            )
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    def get_confirmation_address_markup() -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Подтвердить адрес",
                        callback_data="confirm_address",
                    ),
                    InlineKeyboardButton(
                        text="❌ Отменить",
                        callback_data="basket_pay",
                    ),
                ]
            ]
        )
