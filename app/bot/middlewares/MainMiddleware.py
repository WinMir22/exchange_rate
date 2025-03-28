from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.bot.database.statements.insert import add_user
from app.bot.database.statements.select import check_user


class MainMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        type_event = event.message or event.callback_query or event.chat_member_updated
        if type_event:
            user = type_event.from_user
        else:
            return await handler(event, data)
        data["user_id"] = user.id
        data["full_name"] = user.full_name
        async with self.session_pool() as session:
            await add_user(
                check=await check_user(
                    type_event=type_event,
                    session=session,
                ),
                id=user.id,
                full_name=user.full_name,
                username=user.username,
                session=session,
            )
            data["session"] = session
            return await handler(event, data)
