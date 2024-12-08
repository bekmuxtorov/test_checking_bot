from aiogram.dispatcher.filters.state import State, StatesGroup


class AddDepartment(StatesGroup):
    Name = State()
    Description = State()


class AddTest(StatesGroup):
    TestCode = State()
    FileAddress = State()
    Departmant = State()
    Count = State()
    Answers = State()
    Confirm = State()

class WorkTest(StatesGroup):
    Department = State()
    Choice = State()

class CheckTest(StatesGroup):
    Config = State()
