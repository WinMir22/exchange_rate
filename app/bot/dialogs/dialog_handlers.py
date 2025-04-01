import bisect

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, User
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.database.statements.select import get_currencies
from app.bot.database.statements.update import update_currencies
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


async def favorite_handler(
    call: CallbackQuery, select: Select, mng: DialogManager, item_id: str
) -> None:
    session: AsyncSession = mng.middleware_data["session"]
    rate = await get_currencies(call.from_user.id, session=session)
    if item_id.startswith("✅"):
        element = rate.pop(rate.index(item_id))
        element = element[2:]
        index = bisect.bisect_left(rate, element)
        rate.insert(index, element)
        await update_currencies(call.from_user.id, rate, session)
    else:
        element = "✅ " + rate.pop(rate.index(item_id))
        rate.insert(0, element)
        await update_currencies(call.from_user.id, rate, session)
