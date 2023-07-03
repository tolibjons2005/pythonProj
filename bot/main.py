import logging
from os import getenv
import asyncio
import os
from sqlalchemy import URL

from commands import register_user_commands
from db import BaseModel, create_async_engine, get_session_maker, proceed_schemas
from aiohttp.web import run_app
from aiohttp.web_app import Application

from aioredis import Redis
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from dotenv import load_dotenv
load_dotenv()
TELEGRAM_TOKEN = os.getenv('token')
APP_BASE_URL=os.getenv('webhook_uri')


async def on_startup(bot: Bot, base_url: str):
    await bot.set_webhook(f"{base_url}/webhook")

async def on_shutdown(bot:Bot):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)


    logging.warning('Bye!')


def main():
    bot = Bot(token=TELEGRAM_TOKEN, parse_mode="HTML")
    redis = Redis().from_url('redis://default:4ZxLzxTFackwwN7goksA@containers-us-west-40.railway.app:6460')
    dispatcher = Dispatcher(storage=RedisStorage(redis=redis))
    dispatcher["base_url"] = APP_BASE_URL
    dispatcher.startup.register(on_startup)
    dispatcher.shutdown.register(on_shutdown)





    app = Application()
    app["bot"] = bot


    postgres_url = URL.create(
        'postgresql+asyncpg',
            username='postgres',
            password='20050617',

        host='localhost',
        database='postgres',
        port=5432

    )

    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)
    asyncio.run(proceed_schemas(async_engine, BaseModel.metadata))
    register_user_commands(dispatcher)
    SimpleRequestHandler(
        dispatcher=dispatcher,
        bot=bot, session_maker=session_maker
    ).register(app, path="/webhook")


    setup_application(app, dispatcher, bot=bot)

    run_app(app, host="0.0.0.0", port=443)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    main()