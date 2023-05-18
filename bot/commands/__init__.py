__all__ = ['register_user_commands', 'bot_commands']

# from bot.middlewares.register_check import RegisterCheck
from aiogram import Router
from aiogram.filters.command import CommandStart
from commands.start import start
from commands.help import help_func, call_help_func, some_function
from commands.settings import settings_command, settings_callback
from commands.register import send_file, register_group_name, detect_subject, select_subject, \
    tutorial, register_t_name, registered_menu, register_school_name, register_subject, register_students, \
    about_register_students, register_back, get_file, scan_test, register_region, register_district, callback_back, \
    reg_menu, about_scan_test, select_group_name, add_scor, edit_add_students, edit_datas, get_stats, select_role, student_menu, result_msg, select_sub_name, register_new_group_name, \
    new_detect_subject,register_new_group_name,new_about_register_st

from aiogram import F
from commands.callback_data_states import TestCallbackData
from fsm import Registration, PostRegistration

from commands.register import select_test_type

bot_commands = (('start', 'Start  starts', 'Start  starts bot'),
                ('help', 'Help  helps', 'Help  help bot'))


def register_user_commands(router: Router) -> None:
    # router.message.register(show_user)
    # router.message.register(add_scor, CommandStart())
    # router.message.register(send_mes, CommandStart())
    router.message.register(register_subject, F.text == 'Ortga qaytish🔙', Registration.register_group_name)
    router.message.register(register_back, F.text == "Ortga qaytish🔙")

    router.message.register(reg_menu, CommandStart(),PostRegistration.menu)
    router.message.register(reg_menu, CommandStart(), PostRegistration.scan_test)
    router.message.register(reg_menu, CommandStart(), PostRegistration.send_file)
    router.message.register(reg_menu, CommandStart(), PostRegistration.edit_datas)


    router.message.register(register_new_group_name, F.text == 'Yangi guruh qo\'shish', PostRegistration.edit_datas)
    router.message.register(select_group_name, F.text == 'O\'quvchi qo\'shish', PostRegistration.edit_datas)
    router.message.register(edit_datas, F.text == 'Qo\'shishni yakunlash',  PostRegistration.register_students_new)
    router.message.register(edit_datas, F.text == 'Qo\'shishni yakunlash', PostRegistration.add_students)
    router.message.register(edit_datas, F.text == 'Ma\'lumotlarni tahrirlash✏️', PostRegistration.menu)
    router.message.register(select_group_name, F.text == 'Statistika📊', PostRegistration.menu)
    router.message.register(select_group_name,F.text=='Test yaratish📝', PostRegistration.menu)
    router.message.register(about_scan_test, F.text=='Natijalarni tekshirish✅❌', PostRegistration.menu)

    router.callback_query.register(edit_add_students, F.data.startswith('gr_'),PostRegistration.edit_datas)


    router.callback_query.register(select_test_type, F.data.startswith('gr_'))
    router.callback_query.register(get_stats, F.data.startswith('test_type_'), PostRegistration.stats)
    router.callback_query.register(send_file, F.data.startswith('test_type_'))




    router.callback_query.register(register_group_name, F.data.startswith('data'), Registration.register_subject)
    router.callback_query.register(register_new_group_name, F.data == ('detect_back'), PostRegistration.new_gr)
    router.callback_query.register(register_group_name, F.data==('detect_back'))
    router.callback_query.register(register_school_name, F.data=='region_back')
    router.callback_query.register(register_district, F.data.startswith('region'))
    router.callback_query.register(register_region, F.data.startswith('subject_back'))

    router.callback_query.register(register_region, F.data=='district_back')

    router.message.register(new_detect_subject, PostRegistration.new_gr)
    router.message.register(detect_subject, Registration.register_group_name)
    router.callback_query.register(new_detect_subject, F.data == 'select_back', PostRegistration.new_gr)
    router.callback_query.register(detect_subject, F.data=='select_back')
    router.callback_query.register(select_subject, F.data.endswith('subject'))
    router.callback_query.register(register_region, F.data == 'district_back')
    router.callback_query.register(new_about_register_st, F.data.startswith('sub_s_'), PostRegistration.new_gr)
    router.callback_query.register(about_register_students, F.data.startswith('sub_s_'))

    router.message.register(tutorial, CommandStart())
    router.message.register(reg_menu, F.text == 'Asosiy menyuga qaytish🔙', PostRegistration.send_file)
    router.message.register(reg_menu, F.text == 'Asosiy menyuga qaytish🔙', PostRegistration.scan_test)
    router.message.register(reg_menu, F.text == 'Asosiy menyuga qaytish🔙', PostRegistration.edit_datas)
    router.message.register(reg_menu, F.text == 'Ro‘yxatdan o‘tishni yakunlash',Registration.end)
    router.message.register(registered_menu, F.text == "Qo'shishni yakunlash", Registration.register_students)
    router.message.register(select_role, F.text == "O‘rganib chiqdim", Registration.tutorial)
    router.message.register(student_menu, F.text == "O‘quvchi", Registration.slkt_role)
    router.message.register(select_sub_name, F.text == "Ohirgi natijani ko‘rish", Registration.show_res)
    router.callback_query.register(result_msg,  F.data.startswith('sub_'), Registration.show_res)

    router.message.register(register_t_name, F.text == "O‘qituvchi", Registration.slkt_role)
    router.message.register(register_school_name, Registration.register_t_name)

    router.message.register(register_region, Registration.register_school_name)
    router.callback_query.register(register_subject,F.data.startswith('district'))
    router.message.register(register_students, PostRegistration.register_students_new)
    router.message.register(register_students, PostRegistration.add_students)

    router.message.register(register_students, Registration.register_students)
    router.message.register(register_back, F.text == "Ortga qaytish🔙")
    router.message.register(get_file, F.document,PostRegistration.send_file, flags={"long_operation":"upload_document"})
    router.message.register(scan_test, F.photo, PostRegistration.scan_test)




    # router.message.register(RegisterCheck())
    # router.callback_query.register(RegisterCheck())
