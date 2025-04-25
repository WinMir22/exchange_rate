import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager

from app.bot.dialogs.dialogs_states import StartSG

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def start_command(
    message: Message, user_id: int, full_name: str, manager: DialogManager
) -> None:
    await manager.start(state=StartSG.start)
    logger.info(f"Пользователь {full_name}({user_id}) запустил бота")
