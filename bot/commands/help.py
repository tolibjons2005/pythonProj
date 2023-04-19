from aiogram import types
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from sqlalchemy import select  # type: ignore
from sqlalchemy.orm import sessionmaker, joinedload, selectinload  # type: ignore
from fsm import Registration
# from bot.db.user import get_user, create_user


async def help_func(message: types.Message, session_maker: sessionmaker):
    await message.answer("jkjkjakdakdakjdkamdkaj")



async def call_help_func(call: types.CallbackQuery):
    await call.message.edit_text("jkjkjakdakdakjdkamdkaj", reply_markup=call.message.reply_markup)


async def some_function(message: types.Message, session_maker: sessionmaker, state: FSMContext):
    pass

