import logging
from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from app.bot.lexicon.lexicon_ru import lexicon
from app.bot.states.states import FSMExchangeRate
from app.services.https_requests import get_exchange_rate

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def start_command(message: Message):
    name, user_id = message.from_user.full_name, message.from_user.id
    await message.answer(lexicon["start_command"])
    logger.info(f"Пользователь {name}({user_id}) запустил бота")


@router.message(Command("help"))
async def help_command(message: Message):
    name, user_id = message.from_user.full_name, message.from_user.id
    await message.answer(lexicon["help_command"])
    logger.info(f"Пользователь {name}({user_id}) вызвал команду хелп")


@router.message(Command("exchange_rate"))
async def get_exchange_rate_command(message: Message, state: FSMContext):
    name, user_id = message.from_user.full_name, message.from_user.id
    await state.set_state(state=FSMExchangeRate.get_code_for_check)
    await message.answer(lexicon["exchange_rate_command"])
    logger.info(
        f"Пользователь {name}({user_id}) перешёл в состояние get_code_for_check"
    )


@router.message(FSMExchangeRate.get_code_for_check)
async def give_exchange_rate_command(message: Message, state: FSMContext):
    name, user_id = message.from_user.full_name, message.from_user.id
    try:
        rate = await get_exchange_rate(message.text)
        await state.clear()
        await message.answer(rate)
        logger.info(f"Пользователь {name}({user_id}) узнал валюту {message.text}")
    except KeyError:
        await message.answer(lexicon["exchange_rate_error"])
        logger.info(
            f"Пользователь {name}({user_id}) попытался узнал валюту {message.text}"
        )
