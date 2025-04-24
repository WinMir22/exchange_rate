from aiogram.types import User
from aiogram_dialog import DialogManager
from sqlalchemy.ext.asyncio import AsyncSession

from app.bot.database.db_class import DatabaseCRUD
from app.services.exchange_rate_services.https_requests import get_exchange_rate


async def to_usd_getter(
    event_from_user: User,
    database_crud: DatabaseCRUD,
    dialog_manager: DialogManager,
    **kwargs
):
    data = dialog_manager.dialog_data
    if data["check_rate"].startswith("✅"):
        data["check_rate"] = data["check_rate"][2:]
    result = await get_exchange_rate(check_code=data["check_rate"], give_code="usd")
    return {
        "rates": await database_crud.get_currencies(event_from_user.id),
        "result": result,
        "check": data["check_rate"],
    }


async def rate_getter(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.dialog_data
    if data["check_rate"].startswith("✅"):
        data["check_rate"] = data["check_rate"][2:]
    if data["give_rate"].startswith("✅"):
        data["give_rate"] = data["give_rate"][2:]
    if data["value"].startswith("✅"):
        data["value"] = data["value"][2:]
    result = await get_exchange_rate(
        check_code=data["check_rate"], give_code=data["give_rate"]
    )
    return {
        "result": result,
        "value": data["value"],
    }


async def rates_getter(
    dialog_manager: DialogManager,
    event_from_user: User,
    database_crud: DatabaseCRUD,
    **kwargs
):
    return {"rates": await database_crud.get_currencies(event_from_user.id)}
