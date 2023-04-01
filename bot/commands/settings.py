from aiogram import types
from aiogram.utils.keyboard import (InlineKeyboardBuilder)

from bot.commands.callback_data_states import TestCallbackData


async def settings_command(message: types.Message):
    settings_markup = InlineKeyboardBuilder()
    settings_markup.button(
        text="Yandex",
        url='yandex.ru'
    )
    settings_markup.button(
        text='Settings',
        callback_data='help'
        # callback_data=TestCallbackData(text="test", user_id=message.from_user.id)
    )

    await message.answer("Settings", reply_markup=settings_markup.as_markup())

async def settings_callback(call: types.CallbackQuery, callback_data: TestCallbackData):
    await call.message.answer(callback_data.text + ', ' + str(callback_data.user_id))
