from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from filters.CALL_DATA import ChoosesCallbackFactory

async def get_keyboard_fab(ans_list, page_number, test_type):
    builder = InlineKeyboardBuilder()
    if page_number == 0:
        choosl='ABCD'
        cn=0
        for i in ans_list[:15]:
            if i ==5:
                builder.row(types.InlineKeyboardButton(text=f"{cn+1}", callback_data=ChoosesCallbackFactory(action="notSelective").pack()))
                builder.add(types.InlineKeyboardButton(text=f"A", callback_data=ChoosesCallbackFactory(action="select", column_n=cn, row_n=0, page_num=0).pack()))
                builder.add(types.InlineKeyboardButton(text=f"B", callback_data=ChoosesCallbackFactory(action="select", column_n=cn, row_n=1, page_num=0).pack()))
                builder.add(types.InlineKeyboardButton(text=f"C", callback_data=ChoosesCallbackFactory(action="select", column_n=cn, row_n=2, page_num=0).pack()))
                builder.add(types.InlineKeyboardButton(text=f"D", callback_data=ChoosesCallbackFactory(action="select", column_n=cn, row_n=3, page_num=0).pack()))
            else:
                builder.row(types.InlineKeyboardButton(text=f"{cn + 1}", callback_data=ChoosesCallbackFactory(action="notSelective").pack()))
                builder.add(types.InlineKeyboardButton(text=f"{choosl[i]}", callback_data=ChoosesCallbackFactory(action="notSelective").pack()))
                builder.add(types.InlineKeyboardButton(text="🔁", callback_data=ChoosesCallbackFactory(action="reselect", column_n=cn, page_num=0).pack()))
            cn+=1
        builder.row(types.InlineKeyboardButton(text=f"Keyingi sahifa", callback_data=ChoosesCallbackFactory(action="nextpage", test_type=test_type, page_num=page_number+1).pack()))
    elif test_type == 30 and page_number==1:
        choosl='ABCD'
        cn=15
        for i in ans_list[15:]:
            if i ==5:
                builder.row(types.InlineKeyboardButton(text=f"{cn+1}", callback_data=ChoosesCallbackFactory(action="notSelective").pack()))
                builder.add(types.InlineKeyboardButton(text=f"A", callback_data=ChoosesCallbackFactory(action="select", column_n=cn, row_n=0, page_num=1).pack()))
                builder.add(types.InlineKeyboardButton(text=f"B", callback_data=ChoosesCallbackFactory(action="select", column_n=cn, row_n=1, page_num=1).pack()))
                builder.add(types.InlineKeyboardButton(text=f"C", callback_data=ChoosesCallbackFactory(action="select", column_n=cn, row_n=2, page_num=1).pack()))
                builder.add(types.InlineKeyboardButton(text=f"D", callback_data=ChoosesCallbackFactory(action="select", column_n=cn, row_n=3, page_num=1).pack()))
            else:
                builder.row(types.InlineKeyboardButton(text=f"{cn + 1}", callback_data=ChoosesCallbackFactory(action="notSelective").pack()))
                builder.add(types.InlineKeyboardButton(text=f"{choosl[i]}", callback_data=ChoosesCallbackFactory(action="notSelective").pack()))
                builder.add(types.InlineKeyboardButton(text="🔁", callback_data=ChoosesCallbackFactory(action="reselect", column_n=cn, page_num=1).pack()))
            cn+=1
        builder.row(types.InlineKeyboardButton(text=f"Oldingi sahifa", callback_data=ChoosesCallbackFactory(action="nextpage", test_type=test_type, page_num=page_number-1).pack()))
        builder.add(types.InlineKeyboardButton(text=f"Yakunlash", callback_data=ChoosesCallbackFactory(action="finish", test_type=test_type,page_num=page_number).pack()))
    elif page_number>0 and page_number<5:
        choosl='ABCD'
        cn=15*page_number
        for i in ans_list[cn:cn+15]:
            if i ==5:
                builder.row(types.InlineKeyboardButton(text=f"{cn+1}", callback_data=ChoosesCallbackFactory(action="notSelective").pack()))
                builder.add(types.InlineKeyboardButton(text=f"A", callback_data=ChoosesCallbackFactory(action="select", column_n=cn, row_n=0, page_num=page_number).pack()))
                builder.add(types.InlineKeyboardButton(text=f"B", callback_data=ChoosesCallbackFactory(action="select", column_n=cn, row_n=1, page_num=page_number).pack()))
                builder.add(types.InlineKeyboardButton(text=f"C", callback_data=ChoosesCallbackFactory(action="select", column_n=cn, row_n=2, page_num=page_number).pack()))
                builder.add(types.InlineKeyboardButton(text=f"D", callback_data=ChoosesCallbackFactory(action="select", column_n=cn, row_n=3, page_num=page_number).pack()))
            else:
                builder.row(types.InlineKeyboardButton(text=f"{cn + 1}", callback_data=ChoosesCallbackFactory(action="notSelective").pack()))
                builder.add(types.InlineKeyboardButton(text=f"{choosl[i]}", callback_data=ChoosesCallbackFactory(action="notSelective").pack()))
                builder.add(types.InlineKeyboardButton(text="🔁", callback_data=ChoosesCallbackFactory(action="reselect", column_n=cn, page_num=page_number).pack()))
            cn+=1
        builder.row(types.InlineKeyboardButton(text=f"Oldingi sahifa", callback_data=ChoosesCallbackFactory(action="nextpage", test_type=test_type, page_num=page_number-1).pack()))
        builder.add(types.InlineKeyboardButton(text=f"Keyingi sahifa", callback_data=ChoosesCallbackFactory(action="nextpage", test_type=test_type, page_num=page_number+1).pack()))
    elif page_number==5:
        choosl='ABCD'
        cn=75
        for i in ans_list[75:90]:
            if i ==5:
                builder.row(types.InlineKeyboardButton(text=f"{cn+1}", callback_data=ChoosesCallbackFactory(action="notSelective").pack()))
                builder.add(types.InlineKeyboardButton(text=f"A", callback_data=ChoosesCallbackFactory(action="select", column_n=cn, row_n=0, page_num=page_number).pack()))
                builder.add(types.InlineKeyboardButton(text=f"B", callback_data=ChoosesCallbackFactory(action="select", column_n=cn, row_n=1, page_num=page_number).pack()))
                builder.add(types.InlineKeyboardButton(text=f"C", callback_data=ChoosesCallbackFactory(action="select", column_n=cn, row_n=2, page_num=page_number).pack()))
                builder.add(types.InlineKeyboardButton(text=f"D", callback_data=ChoosesCallbackFactory(action="select", column_n=cn, row_n=3, page_num=page_number).pack()))
            else:
                builder.row(types.InlineKeyboardButton(text=f"{cn + 1}", callback_data=ChoosesCallbackFactory(action="notSelective").pack()))
                builder.add(types.InlineKeyboardButton(text=f"{choosl[i]}", callback_data=ChoosesCallbackFactory(action="notSelective").pack()))
                builder.add(types.InlineKeyboardButton(text="🔁", callback_data=ChoosesCallbackFactory(action="reselect", column_n=cn, page_num=page_number).pack()))
            cn+=1
        builder.row(types.InlineKeyboardButton(text=f"Oldingi sahifa", callback_data=ChoosesCallbackFactory(action="nextpage", test_type=test_type, page_num=page_number-1).pack()))
        builder.add(types.InlineKeyboardButton(text=f"Yakunlash", callback_data=ChoosesCallbackFactory(action="finish", test_type=test_type,page_num=page_number).pack()))

        

        



    return builder.as_markup()

async def confirm_or_back(test_type, page_number):
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"Tasdiqlash", callback_data=ChoosesCallbackFactory(action="confirm").pack()))

    builder.row(types.InlineKeyboardButton(text=f"Ortga qaytish", callback_data=ChoosesCallbackFactory(action="nextpage", test_type=test_type, page_num=page_number).pack()))
    return builder.as_markup()

async def new_test_type():
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text=f"90 talik (blok)", callback_data=ChoosesCallbackFactory(action="detect_subject").pack()))

    builder.row(types.InlineKeyboardButton(text=f"30 talik", callback_data=ChoosesCallbackFactory(action="send_file30").pack()))
    return builder.as_markup()





