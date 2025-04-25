from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Select

from app.bot.database.db_class import DatabaseCRUD


async def check_rate(
    callback: CallbackQuery,
    select: Select,
    manager: DialogManager,
    item_id: str,
):
    data = manager.dialog_data
    data["check_rate"] = item_id
    await manager.next()


async def give_rate(
    query: CallbackQuery, select: Select, manager: DialogManager, item_id: str
) -> None:
    data = manager.dialog_data
    data["give_rate"], data["value"] = item_id, item_id
    await manager.next()


async def favorite_handler(
    call: CallbackQuery, select: Select, mng: DialogManager, item_id: str
) -> None:
    database_crud: DatabaseCRUD = mng.middleware_data["database_crud"]
    rate = await database_crud.get_currencies(call.from_user.id)

    if item_id.startswith("✅"):
        element = rate.pop(rate.index(item_id))
        clean_element = element[2:]
        starred = [s for s in rate if s.startswith("✅")]
        unstarred = sorted(
            [s for s in rate if not s.startswith("✅")] + [clean_element],
            key=lambda x: x.lower(),
        )
        new_rate = starred + unstarred
    else:
        element = rate.pop(rate.index(item_id))
        starred = sorted(
            [f"✅ {element}"] + [s for s in rate if s.startswith("✅")],
            key=lambda x: x[2:].lower(),
        )
        unstarred = [s for s in rate if not s.startswith("✅")]
        new_rate = starred + unstarred

    await database_crud.update_currencies(call.from_user.id, new_rate)
