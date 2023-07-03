from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv
from aiohttp import web
import os
load_dotenv()
tokn= os.getenv('token')
bot = Bot(token=tokn)
Bot.set_current(bot)

dp = Dispatcher(bot)
app = web.Application()

webhook_path = f'/{tokn}'
async def set_webhook():
    webhook_uri= f"https://70b8-213-230-76-100.ngrok-free.app{webhook_path}"
    await bot.set_webhook(webhook_uri)
async def on_startup(_):
    await set_webhook()

@dp.message_handler(commands=['start'])
async def cmd_start_help(msg: types.Message):
    await msg.answer(text='Hello world')

async def handle_webhook(request):
    url = str(request.url)
    index = url.rfind('/')
    token = url[index+1:]

    if token == tokn:
        request_data = await request.json()
        update= types.Update(**request_data)
        await dp.process_update(update)

        return web.Response()
    else:
        return web.Response(status=403)
app.router.add_post(f'/{tokn}', handle_webhook)

if __name__ == '__main__':
    app.on_startup.append(on_startup)
    web.run_app(app, host='0.0.0.0', port=8080)
