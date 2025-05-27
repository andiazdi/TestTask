from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from models import Product
from .utils import (
    get_category_by_parent_id,
    get_category_parent_id,
    get_products_by_category_id,
)
from math import ceil

PAGE_SIZE = 3


class CatalogMarkup:
    @staticmethod
    async def get_categories_markup(
        parent_id: int = None, page: int = 1
    ) -> InlineKeyboardMarkup:
        categories = await get_category_by_parent_id(parent_id)
        total_pages = ceil(len(categories) / PAGE_SIZE)
        page = max(1, min(page, total_pages))

        start = (page - 1) * PAGE_SIZE
        end = start + PAGE_SIZE
        categories_page = categories[start:end]

        buttons = [
            [
                InlineKeyboardButton(
                    text=category.title,
                    callback_data=f"categories_page_{category.id}_1",
                )
            ]
            for category in categories_page
        ]
        pagination_buttons = []
        for p in range(1, total_pages + 1):
            text = f"{p} 🔘" if p == page else str(p)
            pagination_buttons.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=f"categories_page_{parent_id}_{p}",
                )
            )
        if pagination_buttons and len(pagination_buttons) > 1:
            buttons.append(pagination_buttons)

        if parent_id is not None:
            parent_id = await get_category_parent_id(parent_id)
            buttons.append(
                [
                    InlineKeyboardButton(
                        text="🔙 Назад к категориям",
                        callback_data=f"categories_page_{parent_id}_1",
                    )
                ]
            )

        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    async def get_products_markup(
        category_id: int, page: int = 1
    ) -> InlineKeyboardMarkup:
        products = await get_products_by_category_id(category_id)
        total_pages = ceil(len(products) / PAGE_SIZE)
        page = max(1, min(page, total_pages))

        start = (page - 1) * PAGE_SIZE
        end = start + PAGE_SIZE
        products_page = products[start:end]

        buttons = [
            [
                InlineKeyboardButton(
                    text=product.title,
                    callback_data=f"product_info_{product.id}_{page}",
                )
            ]
            for product in products_page
        ]

        pagination_buttons = []
        for p in range(1, total_pages + 1):
            text = f"{p} 🔘" if p == page else str(p)
            pagination_buttons.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=f"products_page_{category_id}_{p}",
                )
            )

        if pagination_buttons and buttons and len(pagination_buttons) > 1:
            buttons.append(pagination_buttons)

        parent_category_id = await get_category_parent_id(category_id)
        buttons.append(
            [
                InlineKeyboardButton(
                    text="🔙 Назад к категориям",
                    callback_data=f"categories_page_{parent_category_id}_1",
                )
            ]
        )
        return InlineKeyboardMarkup(inline_keyboard=buttons)

    @staticmethod
    async def get_product_details_markup(
        product: Product, page_id: int
    ) -> InlineKeyboardMarkup:
        buttons = [
            [
                InlineKeyboardButton(
                    text="Добавить в корзину 🛒",
                    callback_data=f"add_to_cart_{product.id}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Назад к продуктам",
                    callback_data=f"back_to_products",
                )
            ],
        ]

        return InlineKeyboardMarkup(inline_keyboard=buttons)
