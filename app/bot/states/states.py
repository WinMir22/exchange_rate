from aiogram.fsm.state import StatesGroup, State


class FSMExchangeRate(StatesGroup):
    get_code_for_check = State()
    get_code_for_give = State()
