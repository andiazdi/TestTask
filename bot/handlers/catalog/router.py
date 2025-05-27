from aiogram import Router, F
from aiogram.types import CallbackQuery
from .markups import CatalogMarkup
from .utils import get_product_by_id

router = Router()


@router.message(F.text == "Каталог 🛍")
async def show_catalog(message):
    markup = await CatalogMarkup.get_categories_markup(parent_id=None)
    if not markup.inline_keyboard:
        await message.answer("Каталог пуст.")
        return
    await message.answer("Выберите категорию:", reply_markup=markup)


@router.callback_query(F.data.startswith("categories_page_"))
async def categories_pagination_handler(callback: CallbackQuery):
    category_id, page = callback.data.split("_")[2:]

    if category_id == "None":
        category_id = None
    else:
        category_id = int(category_id)
    markup = await CatalogMarkup.get_categories_markup(
        parent_id=category_id, page=int(page)
    )
    prev_markup = callback.message.reply_markup

    if len(markup.inline_keyboard) > 1 and markup != prev_markup:
        await callback.message.edit_text(
            "Выберите категорию товара:", reply_markup=markup
        )
    else:
        await callback.message.edit_text(
            text="Выберите товар:",
            reply_markup=await CatalogMarkup.get_products_markup(
                category_id=category_id
            ),
        )


@router.callback_query(F.data.startswith("products_page_"))
async def products_pagination_handler(callback: CallbackQuery):
    category_id, page = callback.data.split("_")[2:]
    markup = await CatalogMarkup.get_products_markup(int(category_id), int(page))
    if len(markup.inline_keyboard) > 1:
        await callback.message.edit_text("Выберите товар:", reply_markup=markup)


@router.callback_query(F.data.startswith("product_info_"))
async def product_info_handler(callback: CallbackQuery):
    product_id, page = callback.data.split("_")[2:]
    product_id = int(product_id)
    product = await get_product_by_id(product_id)
    if not product:
        await callback.answer("Товар не найден.")
        return

    markup = await CatalogMarkup.get_product_details_markup(product, page)
    await callback.message.answer_photo(
        photo=product.image_path,
        caption=f"<b>{product.title}</b>\n\n{product.description}\n\nЦена: <b>{product.price}₽</b>",
        reply_markup=markup,
    )


@router.callback_query(F.data == "back_to_products")
async def back_to_products_handler(callback: CallbackQuery):
    try:
        await callback.message.delete()
    except Exception as e:
        pass
