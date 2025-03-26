import logging
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery

from app.bot.keyboards.user_keyboards import more_rate_kb, check_rates_kb
from app.bot.lexicon.lexicon_ru import lexicon
from app.bot.states.states import FSMExchangeRate
from app.services.exchange_rate_services.https_requests import get_exchange_rate
from app.services.exchange_rate_services.list_of_rates import rates

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def start_command(message: Message, user_id, full_name):
    await message.answer(lexicon["start_command"])
    logger.info(f"Пользователь {full_name}({user_id}) запустил бота")


@router.message(Command("help"))
async def help_command(message: Message, user_id: int, full_name: str):
    await message.answer(lexicon["help_command"])
    logger.info(f"Пользователь {full_name}({user_id}) вызвал команду хелп")


@router.message(Command("cancel"), StateFilter(default_state))
async def not_cancel_command(message: Message, user_id: int, full_name: str):
    await message.answer(lexicon["not_cancel_command"])
    logger.info(f"Пользователь {full_name}({user_id}) попытался выйти из состояния")


@router.message(Command("cancel"))
async def cancel_command(
    message: Message, state: FSMContext, user_id: int, full_name: str
):
    await state.clear()
    await message.answer(lexicon["cancel_command"])
    logger.info(f"Пользователь {full_name}({user_id}) вышел из состояния")


@router.message(Command("exchange_rate"))
async def get_exchange_rate_command(
    message: Message, state: FSMContext, full_name: str, user_id: int
):
    await state.set_state(state=FSMExchangeRate.get_code_for_check)
    await message.answer(lexicon["exchange_rate_command"], reply_markup=check_rates_kb)
    logger.info(
        f"Пользователь {full_name}({user_id}) перешёл в состояние get_code_for_check"
    )


@router.callback_query(F.data == "check_rates")
async def check_rates_command(call: CallbackQuery, full_name: str, user_id: int):
    await call.message.answer(", ".join(rates))
    await call.answer()
    logger.info(f"Пользователь {full_name}({user_id}) посмотрел доступные валюты")


@router.message(FSMExchangeRate.get_code_for_check)
async def give_exchange_rate_command(
    message: Message, state: FSMContext, user_id: int, full_name: str
):
    await state.update_data(code_for_check=message.text)
    await state.set_state(state=FSMExchangeRate.get_code_for_give)
    await message.answer(text=lexicon["get_code_for_check_state"])
    logger.info(
        f"Пользователь {full_name}({user_id}) хочет узнать валюту {message.text}"
    )
    logger.info(
        f"Пользователь {full_name}({user_id}) перешёл в состояние get_code_for_give"
    )


@router.message(FSMExchangeRate.get_code_for_give)
async def get_exchange_rate_step2(
    message: Message, state: FSMContext, user_id: int, full_name: str
):
    data = await state.get_data()
    try:
        value = await get_exchange_rate(
            check_code=data["code_for_check"], give_code=message.text
        )
        await message.answer(
            lexicon["exchange_rate_answer_command"].format(value, message.text),
            reply_markup=more_rate_kb,
        )
        await state.clear()
        logger.info(f"Пользователь {full_name}({user_id}) узнал валюту {message.text}")
    except KeyError:
        await message.answer(lexicon["exchange_rate_error"])
        logger.info(
            f"Пользователь {full_name}({user_id}) попытался узнать валюту {message.text}"
        )


@router.callback_query(F.data == "more_rate")
async def get_exchange_rate_command_but(
    callback_query: CallbackQuery, state: FSMContext, user_id: int, full_name: str
):
    await get_exchange_rate_command(
        message=callback_query.message,
        state=state,
        user_id=user_id,
        full_name=full_name,
    )
    await callback_query.answer()
