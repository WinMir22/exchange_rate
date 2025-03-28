from aiogram.fsm.state import StatesGroup, State


class StartSG(StatesGroup):
    start = State()


class OneRateSG(StatesGroup):
    get_rate = State()
    give_rate = State()
    get_result = State()
