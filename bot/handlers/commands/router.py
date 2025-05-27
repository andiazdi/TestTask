from aiogram import Router
from aiogram.filters import CommandStart
from .markups import MainMarkup
from .utils import save_user
import logging

router = Router()


@router.message(CommandStart())
async def start_command_handler(message):
    user = await save_user(message.from_user)
    logging.debug(f"User {message.from_user.id} started the bot.")
    if user:
        logging.debug(f"User {message.from_user.id} saved to the database.")
    await message.answer(
        "Приветствую в нашем магазине 👋",
        reply_markup=MainMarkup.get_main_markup(),
    )
