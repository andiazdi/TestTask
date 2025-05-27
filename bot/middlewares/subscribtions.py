from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message
from aiogram.enums.chat_member_status import ChatMemberStatus
from config import REQUIRED_CHATS, REQUIRED_CHANNELS
from .markups import MiddlewareMarkup


class SubscriptionMiddleware(BaseMiddleware):
    def __init__(self):
        self.required_chats = {
            **REQUIRED_CHATS,
            **REQUIRED_CHANNELS,
        }

    async def __call__(self, handler, event: Message, data: dict):
        for chat_title, chat_id in self.required_chats.items():
            if chat_id.startswith("@"):
                chat_info = f"<a href=t.me/{chat_id[1:]}>{chat_title}</a>"
            else:
                chat_info = f"приватный чат/канал {chat_title}"
            try:
                member = await event.bot.get_chat_member(chat_id, event.from_user.id)
                if member.status in (
                    ChatMemberStatus.KICKED,
                    ChatMemberStatus.LEFT,
                ):
                    await event.answer(
                        f"🔒 Доступ ограничен.\nПодпишитесь на следующий каналы/чаты:",
                        reply_markup=MiddlewareMarkup.get_markup(self.required_chats),
                    )
                    return
            except TelegramBadRequest:
                await event.answer(
                    f"⚠️ Не удалось проверить подписку на {chat_info}",
                )
                return

        return await handler(event, data)
