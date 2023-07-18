import logging
import os
import asyncio
import pstats

from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.types import BotCommand
# from aioredis import Redis
from sqlalchemy.engine import URL
from dotenv import load_dotenv
from redis import asyncio as aioredis

from arq import create_pool
from config import conf


from middlewares.register_check import ChatActionMiddleware
from commands import register_user_commands, bot_commands
from db import BaseModel, create_async_engine, get_session_maker, proceed_schemas

bot_commands= (('start','Start  starts', 'Start  starts bot'),
               ('help','Help  helps', 'Help  help bot'))
async def main() -> None:
    load_dotenv()
    logging.basicConfig(level=logging.DEBUG)

    commands_for_bot = []
    for cmd in bot_commands:
        commands_for_bot.append(BotCommand(command=cmd[0], description=cmd[1]))

    redis = aioredis.Redis().from_url('redis://default:4ZxLzxTFackwwN7goksA@containers-us-west-40.railway.app:6460')
    # redis



    #storage = MemoryStorage()
    dp =Dispatcher(storage=RedisStorage(redis=redis))
    bot = Bot(token=os.getenv('token'))
    dp.message.middleware(ChatActionMiddleware())


    # dp.callback_query.middleware(RegisterCheck())

    # bot = Bot(token=os.getenv('token'))

    await bot.set_my_commands(commands=commands_for_bot)

    register_user_commands(dp)

    postgres_url = URL.create(
            'postgresql+asyncpg',
            username=os.getenv('db_user'),
            password=os.getenv('db_pass'),
            host='localhost',
            database=os.getenv('db_name'),
            port=os.getenv('db_port')

        )

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)
    await proceed_schemas(async_engine, BaseModel.metadata)
    redis_pool= await create_pool(conf.redis.pool_settings)


    await dp.start_polling(bot, session_maker=session_maker, arqredis = redis_pool)


if __name__ == '__main__':
    try:

        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')

