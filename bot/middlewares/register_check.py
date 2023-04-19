# from sqlalchemy import select
# from typing import Callable, Dict, Any, Awaitable, Union
# from aiogram import BaseMiddleware
# from aiogram.types import Message, CallbackQuery
# from sqlalchemy.orm import sessionmaker
# from db import User

# class RegisterCheck(BaseMiddleware):
#
#
#     async def __call__(
#         self,
#         handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
#         event: Message|CallbackQuery,
#         data: Dict[str, Any]
#     ) -> Any:
#         session_maker: sessionmaker = data['session_maker']
#         async with session_maker() as session:
#             async with session.begin():
#                 result = await session.execute(select(User).where(User.user_id == event.from_user.id))
#                 await event.answer(str(result))
#                 print(str(result))
#                 user: User = result.one_or_none()
#                 print(str(data))
#
#
#                 await event.answer(str(user.User.username))
#
#                 if user:
#                     pass
#                 else:
#                     user = User(
#                         user_id=event.from_user.id,
#                         username=event.from_user.full_name
#
#                     )
#                     await session.merge(user)
#                     if isinstance(event, Message):
#                         await event.answer("dsfsTTTTTfsffsfsfsf")
#                     else:
#                         await event.answer("elsedsfsTTTTTfsffsfsfsf")
#
#         return await handler(event, data)

import datetime
from typing import Callable, Awaitable, Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

class ThrottlingMiddleware(BaseMiddleware):
    time_updates: dict[int, datetime.datetime] = {}
    timedelta_limiter: datetime.timedelta = datetime.timedelta(seconds=1)

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        if isinstance(event, (Message, CallbackQuery)):
            user_id = event.from_user.id
            if user_id in self.time_updates.keys():
                if (datetime.datetime.now() - self.time_updates[user_id]) > self.timedelta_limiter:
                    self.time_updates[user_id] = datetime.datetime.now()
                    return await handler(event, data)
            else:
                self.time_updates[user_id] = datetime.datetime.now()
                return await handler(event, data)
