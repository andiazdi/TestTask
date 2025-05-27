from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class MiddlewareMarkup:
    @staticmethod
    def get_markup(chats: dict[str, str]) -> InlineKeyboardMarkup:
        buttons = []
        for chat_title, chat_id in chats.items():
            buttons.append(
                [
                    InlineKeyboardButton(
                        text=chat_title,
                        callback_data="subscribe",
                        url=f"t.me/{chat_id[1:]}",
                    )
                ]
            )
        markup = InlineKeyboardMarkup(inline_keyboard=buttons, row_width=2)
        return markup
