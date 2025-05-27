from aiogram.fsm.state import StatesGroup, State


class BasketState(StatesGroup):
    add_to_basket = State()
    remove_from_basket = State()
    pass_address = State()
