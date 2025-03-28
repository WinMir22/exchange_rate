from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from app.services.exchange_rate_services.https_requests import get_exchange_rate


async def check_rate(
    callback: CallbackQuery,
    select: Select,
    manager: DialogManager,
    item_id: str,
):
    state: FSMContext = manager.middleware_data["state"]
    await state.update_data(check_rate=item_id)
    await manager.next()


async def give_rate(
    callback: CallbackQuery, select: Select, manager: DialogManager, item_id: str
):
    state: FSMContext = manager.middleware_data["state"]
    await state.update_data(give_rate=item_id, value=item_id)
    await manager.next()
