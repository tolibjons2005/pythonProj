__all__ = ['register_user_commands', 'bot_commands']

# from bot.middlewares.register_check import RegisterCheck
from aiogram import Router
from aiogram.filters.command import CommandStart
from aiogram.types import ContentType
from filters.simple_filter import IsRegistered,IsRegisteredNot
from commands.register import upload_photo,get_ststs_on, select_on_test_type,get_fullname_fo,check_inline_response,get_test_code,OMR_checking,about_OMR_checking,check_online_test,enter_channel_link, get_file_on,select_on_test_type,enter_minute,create_ot,send_file_fo30,send_file_fo90,detect_sub_fo,confirm_answer,next_page,retry_answer,test_fabric, test_hand,select_group_name_callback,remove_from_premium, testsch,send_file, register_group_name, detect_subject, select_subject, \
    tutorial, register_t_name, registered_menu, register_school_name, register_subject, register_students, \
    about_register_students, register_back, get_file, scan_test, register_region, register_district, callback_back, \
    reg_menu, about_scan_test, select_group_name,  edit_add_students, edit_datas, get_stats, select_role, student_menu, result_msg, select_sub_name, register_new_group_name, \
    new_detect_subject,register_new_group_name,select_test_type,new_about_register_st,select_book_type, send_file30, about_delete_students, delete_students, pre_checkout_query, successful_payment
from aiogram import F
from filters.CALL_DATA import ChoosesCallbackFactory

from fsm import Registration, PostRegistration,StudentMenu



bot_commands = (('start', 'Start  starts', 'Start  starts bot'),
                ('help', 'Help  helps', 'Help  help bot'))


def register_user_commands(router: Router) -> None:
    router.message.register(upload_photo, F.photo)
    router.message.register(register_subject, F.text == 'Ortga qaytish🔙', Registration.register_group_name)
    router.message.register(register_back, F.text == "Ortga qaytish🔙")
    router.message.register(reg_menu, IsRegistered())
    router.message.register(tutorial, CommandStart())
    router.message.register(get_fullname_fo, StudentMenu.start_own_register)
    router.message.register(edit_datas, IsRegisteredNot('Ma\'lumotlarni tahrirlash✏️'))
    router.message.register(select_group_name, IsRegisteredNot('Statistika📊'))
    router.message.register(select_group_name,IsRegisteredNot('Test yaratish📝'))
    router.message.register(about_scan_test, IsRegisteredNot('Natijalarni tekshirish✅❌'))

    # router.message.register(test_hand, CommandStart())
    router.callback_query.register(test_fabric, ChoosesCallbackFactory.filter(F.action=='select'))
    router.callback_query.register(retry_answer, ChoosesCallbackFactory.filter(F.action == 'reselect'))
    router.callback_query.register(next_page, ChoosesCallbackFactory.filter(F.action == 'nextpage'))
    router.callback_query.register(confirm_answer, ChoosesCallbackFactory.filter(F.action == 'finish'))
    router.callback_query.register(detect_sub_fo, ChoosesCallbackFactory.filter(F.action == 'detect_subject'))
    router.callback_query.register(send_file_fo30, ChoosesCallbackFactory.filter(F.action == 'send_file30'))
    router.callback_query.register(check_inline_response, ChoosesCallbackFactory.filter(F.action == 'confirm'))

    router.callback_query.register(send_file_fo90, F.data.startswith('sub_s_'), PostRegistration.detect_on_subject)

    router.message.register(check_online_test, F.text == "Onlayn test natijasini tekshirish✅❌", Registration.show_res)
    router.message.register(about_OMR_checking, F.text == "Rasmga olish orqali tekshirish📸", StudentMenu.select_m_check_online)
    router.message.register(get_test_code, F.text == "Qo‘lda kiritish orqali tekshirish", StudentMenu.select_m_check_online)
    router.message.register(test_hand, StudentMenu.get_code)


    router.message.register(create_ot, F.text=="Onlayn uchun test yaratish📝" )
    router.message.register(get_ststs_on, F.text == "Onlayn test natijasini olish🧾")
    router.message.register(enter_minute,  PostRegistration.set_hour)
    router.message.register(enter_channel_link,  PostRegistration.set_minute)
    router.message.register(select_on_test_type,  PostRegistration.select_enter_channel_link)



    router.message.register(remove_from_premium, (F.text == '/remove')&(F.from_user.id == 729659100))



    router.pre_checkout_query.register(pre_checkout_query)
    router.message.register(successful_payment, F.content_type == ContentType.SUCCESSFUL_PAYMENT)




    router.message.register(register_new_group_name, F.text == 'Yangi guruh qo‘shish➕', PostRegistration.edit_datas)
    router.message.register(select_group_name, F.text == 'O‘quvchi qo‘shish➕', PostRegistration.edit_datas)
    router.message.register(about_delete_students, F.text == 'O‘quvchini o‘chirish🗑', PostRegistration.edit_datas)
    router.message.register(edit_datas, F.text == 'Qo‘shishni yakunlash',  PostRegistration.register_students_new)
    router.message.register(edit_datas, F.text == 'O‘chirishni yakunlash', PostRegistration.delete_students)
    router.message.register(edit_datas, F.text == 'Qo‘shishni yakunlash', PostRegistration.add_students)

    router.message.register(delete_students,PostRegistration.delete_students)

    router.callback_query.register(edit_add_students, F.data.startswith('gr_'),PostRegistration.edit_datas)
    router.callback_query.register(select_group_name_callback, F.data == 're_choose_gr')


    router.callback_query.register(select_test_type, F.data.startswith('gr_'))
    router.callback_query.register(get_stats, F.data.startswith('test_type_'), PostRegistration.stats)
    router.callback_query.register(select_book_type, F.data.startswith('test_type_90'))
    router.callback_query.register(select_book_type, F.data.startswith('test_type_30'))
    router.callback_query.register(send_file30, F.data.startswith('book30_'))
    router.callback_query.register(send_file, F.data.startswith('book_'))




    router.callback_query.register(register_group_name, F.data.startswith('data'), Registration.register_subject)
    router.callback_query.register(select_on_test_type, F.data == ('detect_back'), PostRegistration.detect_on_subject)
    router.callback_query.register(register_new_group_name, F.data == ('detect_back'), PostRegistration.post_new_gr)
    router.callback_query.register(register_group_name, F.data==('detect_back'))
    router.callback_query.register(register_school_name, F.data=='region_back')
    router.callback_query.register(register_district, F.data.startswith('region'))
    router.callback_query.register(register_region, F.data.startswith('subject_back'))

    router.callback_query.register(register_region, F.data=='district_back')

    router.message.register(new_detect_subject, PostRegistration.new_gr)
    router.message.register(detect_subject, Registration.register_group_name)
    router.callback_query.register(select_on_test_type, F.data == 'select_back', PostRegistration.detect_on_subject)
    router.callback_query.register(new_detect_subject, F.data == 'select_back', PostRegistration.post_new_gr)
    router.callback_query.register(detect_subject, F.data=='select_back')
    router.callback_query.register(select_subject, F.data.endswith('subject'))
    router.callback_query.register(register_region, F.data == 'district_back')
    router.callback_query.register(new_about_register_st, F.data.startswith('sub_s_'), PostRegistration.post_new_gr)
    router.callback_query.register(about_register_students, F.data.startswith('sub_s_'))


    router.message.register(reg_menu, F.text == 'Asosiy menyuga qaytish🔙', PostRegistration.send_file)
    router.message.register(reg_menu, F.text == 'Asosiy menyuga qaytish🔙', PostRegistration.scan_test)
    router.message.register(reg_menu, F.text == 'Asosiy menyuga qaytish🔙', PostRegistration.edit_datas)
    router.message.register(reg_menu, F.text == 'Davom etish⏩',Registration.end)
    router.message.register(registered_menu, F.text == "Qo‘shishni yakunlash", Registration.register_students)
    router.message.register(select_role, F.text == "O‘rganib chiqdim", Registration.tutorial)
    router.message.register(student_menu, F.text == "Bo‘lajak talaba👨‍🎓👩‍🎓", Registration.slkt_role)
    router.message.register(select_sub_name, F.text == "Ohirgi natijani ko‘rish", Registration.show_res)
    router.callback_query.register(result_msg,  F.data.startswith('sub_'), Registration.show_res)

    router.message.register(register_t_name, F.text == "Ustoz👨‍🏫👩‍🏫", Registration.slkt_role)
    router.message.register(register_school_name, Registration.register_t_name)

    router.message.register(register_region, Registration.register_school_name)
    router.callback_query.register(register_subject,F.data.startswith('district'))
    router.message.register(register_students, PostRegistration.register_students_new)
    router.message.register(register_students, PostRegistration.add_students)

    router.message.register(register_students, Registration.register_students)
    # router.message.register(register_back, F.text == "Ortga qaytish🔙")
    router.message.register(get_file, F.document,PostRegistration.send_file, flags={"long_operation":"upload_document"})
    router.message.register(scan_test, F.photo, PostRegistration.scan_test)
    router.message.register(OMR_checking, F.photo, StudentMenu.scan_omr)

    router.message.register(get_file_on, F.document,PostRegistration.send_file_on, flags={"long_operation":"upload_document"})





    # router.message.register(RegisterCheck())
    # router.callback_query.register(RegisterCheck())
