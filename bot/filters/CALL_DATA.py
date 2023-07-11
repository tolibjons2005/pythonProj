from typing import Optional
from aiogram.filters.callback_data import CallbackData

class ChoosesCallbackFactory(CallbackData, prefix="choose"):
    action:str
    column_n: Optional[int]
    row_n: Optional[int]
    test_type: Optional[int]
    page_num: Optional[int]
