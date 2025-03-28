from aiogram.fsm.context import FSMContext
from aiogram_dialog import DialogManager

from app.services.exchange_rate_services.https_requests import get_exchange_rate


async def rate_getter(dialog_manager: DialogManager, **kwargs):
    state: FSMContext = dialog_manager.middleware_data["state"]
    data = await state.get_data()
    result = await get_exchange_rate(
        check_code=data["check_rate"], give_code=data["give_rate"]
    )
    return {"result": result, "value": data["value"]}
