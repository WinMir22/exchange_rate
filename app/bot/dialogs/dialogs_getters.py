from aiogram.fsm.context import FSMContext
from aiogram.types import User
from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.database.statements.select import get_currencies
from app.services.exchange_rate_services.https_requests import get_exchange_rate


async def to_usd_getter(
    event_from_user: User,
    session: AsyncSession,
    dialog_manager: DialogManager,
    **kwargs
):
    state: FSMContext = dialog_manager.middleware_data["state"]
    data = await state.get_data()
    result = await get_exchange_rate(check_code=data["check_rate"], give_code="usd")
    return {
        "rates": await get_currencies(event_from_user.id, session=session),
        "result": result,
        "check": data["check_rate"],
    }


async def rate_getter(
    event_from_user: User,
    session: AsyncSession,
    dialog_manager: DialogManager,
    **kwargs
):
    state: FSMContext = dialog_manager.middleware_data["state"]
    data = await state.get_data()
    result = await get_exchange_rate(
        check_code=data["check_rate"], give_code=data["give_rate"]
    )
    return {
        "result": result,
        "rates": await get_currencies(event_from_user.id, session=session),
        "value": data["value"],
        "check": data["check_rate"],
    }


async def rates_getter(
    dialog_manager: DialogManager,
    event_from_user: User,
    session: AsyncSession,
    **kwargs
):
    return {"rates": await get_currencies(event_from_user.id, session=session)}
