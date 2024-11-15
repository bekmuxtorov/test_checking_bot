from aiogram.dispatcher.filters.state import State, StatesGroup


class Registration(StatesGroup):
    full_name = State()
    phone_number = State()
    position = State()
