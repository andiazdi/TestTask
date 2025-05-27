from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class MainMarkup:
    @staticmethod
    def get_main_markup() -> ReplyKeyboardMarkup:
        buttons = (
            KeyboardButton(text="Каталог 🛍"),
            KeyboardButton(text="Корзина 🛒"),
        )
        markup = ReplyKeyboardMarkup(keyboard=[buttons], row_width=2)
        return markup
