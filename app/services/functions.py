from aiogram.types import TelegramObject


def get_from_user(event: TelegramObject) -> TelegramObject:
    if hasattr(event, "message"):
        type_event = event.message
    elif hasattr(event, "callback_query"):
        type_event = event.callback_query
    elif hasattr(event, "chat_member_updated"):
        type_event = event.chat_member_updated
    else:
        type_event = None
    return type_event.from_user
