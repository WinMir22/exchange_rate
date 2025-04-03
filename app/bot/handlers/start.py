import logging
from aiogram import Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager

from app.bot.dialogs.dialogs_states import StartSG
from app.bot.keyboards.user_keyboards import more_rate_kb, check_rates_kb
from app.bot.lexicon.lexicon_ru import lexicon
from app.bot.states.states import FSMExchangeRate
from app.services.exchange_rate_services.https_requests import get_exchange_rate
from app.services.exchange_rate_services.list_of_rates import rates

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def start_command(
    message: Message, user_id: int, full_name: str, dialog_manager: DialogManager
) -> None:
    await dialog_manager.start(state=StartSG.start)
    logger.info(f"Пользователь {full_name}({user_id}) запустил бота")
