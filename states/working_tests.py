from aiogram.dispatcher.filters.state import State, StatesGroup


class AddTest(StatesGroup):
    TestCode = State()
    Count = State()
    Answers = State()
    Confirm = State()
