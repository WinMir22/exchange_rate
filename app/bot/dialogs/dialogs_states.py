from aiogram.fsm.state import StatesGroup, State


class StartSG(StatesGroup):
    start = State()


class OneRateSG(StatesGroup):
    main = State()
