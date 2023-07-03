from typing import Union, Dict, Any

from aiogram.filters import BaseFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext


class IsRegistered(BaseFilter):
    async def __call__(self, message:Message,state: FSMContext):

        # # Если entities вообще нет, вернётся None,
        # # в этом случае считаем, что это пустой список
        # entities = message.entities or []
        #
        # # Проверяем любые юзернеймы и извлекаем их из текста
        # # методом extract(). Подробнее см. главу
        # # про работу с сообщениями
        # found_usernames = [
        #     item.extract_from(message.text) for item in entities
        #     if item.type == "mention"
        # ]
        #
        # # Если юзернеймы есть, то "проталкиваем" их в хэндлер
        # # по имени "usernames"
        state_name=await state.get_state()
        if state_name.startswith('PostRegistration') and message.text=="/start":
            return True
        # Если не нашли ни одного юзернейма, вернём False
        return False