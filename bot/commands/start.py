from aiogram import types


from aiogram.utils.keyboard import (ReplyKeyboardBuilder, KeyboardButton, KeyboardButtonPollType)


async def start(message: types.Message) -> None:
    menu_builder = ReplyKeyboardBuilder()
    menu_builder.button(text="Start")
    menu_builder.add(KeyboardButton(text="Kontakt jo'nat", request_contact=True))
    menu_builder.row(KeyboardButton(text="Poll jo'natish", request_poll=KeyboardButtonPollType()))

    await message.answer('Salom', reply_markup=menu_builder.as_markup(resize_keyboard=True))
