from aiogram import Bot
from arq import cron
from bot.config import conf
from sqlalchemy.orm import sessionmaker
from bot.db.user import get_expired_users
from bot.__main__ import session_maker
async def startup(ctx):
    ctx['bot'] = Bot(token='6148347706:AAEjBM7iqpXxKba1Y5hx615Do8ERUinp6Fg')

async def shutdown(ctx):
    await ctx['bot'].session.close()


async def send_message(ctx, chat_id: int, text:str):
    bot: Bot = ctx['bot']
    await bot.send_message(chat_id, text)

async def plan_mssage(ctx):
    await get_expired_users(sessionmaker)
class WorkerSettings:
    redis_settings = conf.redis.pool_settings
    on_startup = startup
    on_shutdown = shutdown
    functions = [send_message]
    cron_jobs=[
        cron(coroutine="bot.scheduler.main.plan_mssage", second=0)
    ]