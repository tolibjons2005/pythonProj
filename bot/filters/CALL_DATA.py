from typing import Optional
from aiogram.filters.callback_data import CallbackData

class ChoosesCallbackFactory(CallbackData, prefix="choose"):
    action:str
    column_n: Optional[int]=None
    row_n: Optional[int]=None
    test_type: Optional[int]=None
    page_num: Optional[int]=None
