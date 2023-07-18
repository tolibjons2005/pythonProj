import asyncio
import re


from aiogram import types
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from arq import ArqRedis
from sqlalchemy import select  # type: ignore
from sqlalchemy.orm import sessionmaker, joinedload, selectinload, Session  # type: ignore
from fsm import Registration, PostRegistration, StudentMenu
# from bot.keyboards import clear, yes, back, end, keyboard, k_karakalpak, k_andijon, k_bukhara, k_jizzakh, k_qashqadaryo, k_A_NAVOIY, k_namangan, k_samarkand, k_surxondaryo, k_sirdaryo, k_tashkent_reg, k_fergana, k_xorazm, k_tashkent_city, k_regions,
from keyboards import *
from keyboards.reply import menu, back_2_menu, end_register, edit_menu, slct_role, student_key

from pdftool.string2pdf import create_title
from test_scanner.scanner import test_scanner_func,test_scanner_fo
from io import BytesIO
from aiogram import html
from filters.CALL_DATA import ChoosesCallbackFactory
from pdftool.create_title_fo import create_title_on
from pdftool.pdf_online_test import create_pdf_on
from aiogram import Bot

from openpyxl import Workbook

from db.user import change_is_used,is_used_checker,get_online_stats,register_student_fof,can_i_use,get_answers_oo,get_schname_tsub, wr_starter_db,is_group_active,premium_checker,get_expired_users,expire_date,create_user, get_st_ids, get_st_datas, add_answers, get_group_names, add_score, get_st_scores, \
     get_st_dats, get_ans_message, get_sub_names, get_t_sub, count_students, delete_student_r, add_to_dict, is_registered

from pdftool.utils import create_pdf

from db.user import get_stat
from keyboards.reply import test_type
from datetime import date, timedelta
import datetime
import time
import numpy as np

today = date.today()

# dd/mm/YY
d1 = today.strftime("%d.%m.%Y")

# async def send_mes(message: types.Message,bot: Bot):
#     await bot.send_message(1357099819,"Hello")
async def upload_photo(message: types.Message):
    await message.answer(message.photo[-1].file_id)
    await message.answer_photo(message.photo[-1].file_id)
async def get_ststs_on(message:types.Message, session_maker:sessionmaker, bot:Bot):
    res=await get_online_stats(message.from_user.id, session_maker)
    if res == 2:
        await message.answer('Natijalar topilmadi. Hali bironta ham natija tekshirilmagan yoki onlayn test yaratilmagan.')
    elif res == 1:
        await message.answer(
            'Siz bepul tarifdasiz! Shu sababli Premium tarif rasmiylashtirmaguningizgacha onlayn test natijasini ola olmaysiz.\n\n'
            'Premium tarif rasmiylashtirganingizdan so‘ng siz imkoniyatlaringizni ikki barobar ko‘paytirasiz, ya\'ni 4 tagacha guruh, har bir guruhga 30 tagacha odam qo‘shish, <b>onlayn test o‘tkazish</b> imkoniyatiga ega bo‘lasiz '
            'va <b>eng asosiysi loyihani davom etishi va siz uchun yangidan-yangi imkoniyatlar yaratishimiz uchun katta yordam berasiz</b>\n\n'
            '<i>Quyida tarifni tanlab, Click to‘lov tizimi orqali to‘lovni amalga oshirishingiz</i>',
            parse_mode="HTML"
        )
        await bot.send_invoice(
            chat_id=message.from_user.id,
            title='30 kunlik Premiumni sotib olish',
            description='Premiumni rasmiylashtirish uchun karta ma\'lumotlaringizni kiriting ',
            payload='premium30',
            provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065',
            currency='UZS',
            prices=[
                types.LabeledPrice(
                    label="Premium tarifi",
                    amount=2000000
                )
            ],
            need_name=True

        )
        await bot.send_invoice(
            chat_id=message.from_user.id,
            title='1 kunlik Premiumni sotib olish',
            description='Premiumni rasmiylashtirish uchun karta ma\'lumotlaringizni kiriting ',
            payload='premium1',
            provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065',
            currency='UZS',
            prices=[
                types.LabeledPrice(
                    label="Premium tarifi",
                    amount=500000
                )
            ],
            need_name=True

        )
    else:


        # Create a new workbook
        workbook = Workbook()

        # Access the active sheet
        sheet = workbook.active


        # Set the width of column A to 20 characters
        sheet.column_dimensions['A'].width = 25
        sheet.column_dimensions['B'].width = 20
        sheet.column_dimensions['C'].width = 30
        sheet['A1'] = 'O‘quvchi ism-familiyasi'
        sheet['B1'] = 'To‘plagan bali'
        sheet['C1'] = 'Tekshirgan vaqti'
        l=1

        for i in res:
            l+=1
            sheet[f'A{l}'] = i[2]
            sheet[f'B{l}'] = i[1]
            sheet[f'C{l}'] = i[3]






        # Save the workbook as bytes
        bytes_io = BytesIO()
        workbook.save(bytes_io)
        bytes_value = bytes_io.getvalue()
        document = types.input_file.BufferedInputFile(file=bytes_value, filename='@ce_test_center_bot.xlsx')
        await bot.send_document(message.chat.id, document=document)


async def create_ot(message: types.Message, state:FSMContext, session_maker: sessionmaker):
    is_premium = await premium_checker(message.from_user.id, session_maker)
    is_used=await is_used_checker(message.from_user.id, session_maker)
    if not is_used and not is_premium:
        await message.answer(
                               'Siz bepul tarifdasiz! Shu sababli Premium tarif rasmiylashtirmaguningizgacha bot yordamida onlayn test ola olmaysiz.\n\n'
                               'Premium tarif rasmiylashtirganingizdan so‘ng siz imkoniyatlaringizni ikki barobar ko‘paytirasiz, ya\'ni 4 tagacha guruh, har bir guruhga 30 tagacha odam qo‘shish, <b>onlayn test o‘tkazish</b> imkoniyatiga ega bo‘lasiz '
                               'va <b>eng asosiysi loyihani davom etishi va siz uchun yangidan-yangi imkoniyatlar yaratishimiz uchun katta yordam berasiz</b>\n\n'
                               '<i>Quyida tarifni tanlab, Click to‘lov tizimi orqali to‘lovni amalga oshirishingiz yoki onlayn testni bepul olish uchun bir marta beriladigan imkoniyatdan foydalanishingiz mumkin</i>',
                               parse_mode="HTML"
                               )
        await message.answer_invoice(

            title='30 kunlik Premiumni sotib olish',
            description='Premiumni rasmiylashtirish uchun karta ma\'lumotlaringizni kiriting ',
            payload='premium30',
            provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065',
            currency='UZS',
            prices=[
                types.LabeledPrice(
                    label="Premium tarifi",
                    amount=2000000
                )
            ],
            need_name=True)
        await message.answer_invoice(

            title='1 kunlik Premiumni sotib olish',
            description='Premiumni rasmiylashtirish uchun karta ma\'lumotlaringizni kiriting ',
            payload='premium1',
            provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065',
            currency='UZS',
            prices=[
                types.LabeledPrice(
                    label="Premium tarifi",
                    amount=500000
                )
            ],
            need_name=True)
        await message.answer(
            'Agar onlayn testni bepul olish imkoniyatidan foydalanmoqchi bo‘lsangiz qancha vaqt ichida sizning testingizni tekshirish mumkinligini yozing?\n\n<i>Soatni faqat raqamlarda kiriting, '
            'agar 1 soatdan kam vaqtni ichida tekshirish mumkin bo‘lsa 0 ni yuboring</i>', parse_mode="HTML")
        await state.update_data(expire_date=[])
        await state.set_state(PostRegistration.set_hour)
    elif is_premium:
        await message.answer(
            'Qancha vaqt ichida sizning testingizni tekshirish mumkin?\n\n<i>Soatni faqat raqamlarda kiriting, '
            'agar 1 soatdan kam vaqtni ichida tekshirish mumkin bo‘lsa 0 ni yuboring</i>', parse_mode="HTML")
        await state.update_data(expire_date=[])
        await state.set_state(PostRegistration.set_hour)
    elif is_used:
        await message.answer(
            'Siz onlayn testni bepul olish uchun bir marta beriladigan imkoniyatdan foydalanib  bo‘lgansiz! Shu sababli Premium tarif rasmiylashtirmaguningizgacha bot yordamida onlayn test ola olmaysiz.\n\n'
            'Premium tarif rasmiylashtirganingizdan so‘ng siz imkoniyatlaringizni ikki barobar ko‘paytirasiz, ya\'ni 4 tagacha guruh, har bir guruhga 30 tagacha odam qo‘shish, <b>onlayn test o‘tkazish</b> imkoniyatiga ega bo‘lasiz '
            'va <b>eng asosiysi loyihani davom etishi va siz uchun yangidan-yangi imkoniyatlar yaratishimiz uchun katta yordam berasiz</b>\n\n'
            '<i>Quyida kerakli tarifni tanlab, Click to‘lov tizimi orqali to‘lovni amalga oshirishingiz mumkin</i>',
            parse_mode="HTML"
        )
        await message.answer_invoice(

            title='30 kunlik Premiumni sotib olish',
            description='Premiumni rasmiylashtirish uchun karta ma\'lumotlaringizni kiriting ',
            payload='premium30',
            provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065',
            currency='UZS',
            prices=[
                types.LabeledPrice(
                    label="Premium tarifi",
                    amount=2000000
                )
            ],
            need_name=True)
        await message.answer_invoice(

            title='1 kunlik Premiumni sotib olish',
            description='Premiumni rasmiylashtirish uchun karta ma\'lumotlaringizni kiriting ',
            payload='premium1',
            provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065',
            currency='UZS',
            prices=[
                types.LabeledPrice(
                    label="Premium tarifi",
                    amount=500000
                )
            ],
            need_name=True)

  
async def enter_minute(message:types.Message, state:FSMContext):
    pattern = '^\d$|^\d\d$'
    result= re.match(pattern,message.text)
    if result:
        user_data = await state.get_data()

        expire_date = user_data['expire_date']
        expire_date.append(int(message.text))
        await state.update_data(expire_date=expire_date)
        await message.answer(
            'Qancha vaqt ichida sizning testingizni tekshirish mumkin?\n\n<i>Daqiqani faqat raqamlarda kiriting</i>', parse_mode="HTML")
        await state.set_state(PostRegistration.set_minute)
    else:
        await message.answer(
            'Soat xato kiritildi.\n\n<i>Soatni faqat raqamlarda qaytadan kiriting</i>',
            parse_mode="HTML")
async def enter_channel_link(message:types.Message, state:FSMContext):
    pattern = '^\d$|^\d\d$'
    result = re.match(pattern, message.text)
    if result:
        user_data = await state.get_data()

        expire_date = user_data['expire_date']
        expire_date.append(int(message.text))
        await state.update_data(expire_date=expire_date)
        await message.answer(
            '<i>Testni joylamoqhi bo‘lgan kanalingiz linkini kiriting:</i>\n\nMisol uchun: t.me/card_ed',
            parse_mode="HTML")
        await state.set_state(PostRegistration.select_enter_channel_link)
    else:
        await message.answer(
            'Daqiqa xato kiritildi.\n\n<i>Daqiqani faqat raqamlarda qaytadan kiriting</i>',
            parse_mode="HTML")
async def select_on_test_type(message:types.Message|types.CallbackQuery, state:FSMContext):
    # try:
    pattern = '^(t\.me\/)....+'
    result = re.match(pattern, message.text)
    if result:
        await state.update_data(channel_link=message.text)

        await message.answer(
            '<i>Onlayn test olish uchun test shaklini tanlang:</i>',
            parse_mode="HTML", reply_markup=await new_test_type())
        await state.set_state(PostRegistration.select_on_test_type)
    else:
        await message.answer(
            'Kanal linki xato kiritildi.\n\n<i>Kanal linkini t.me/kanalingiz_uzerneymi shu shaklda qaytadan kiriting</i>',
            parse_mode="HTML")
    # except:
    #     await message.message.answer(
    #         '<i>Onlayn test olish uchun test shaklini tanlang:</i>',
    #         parse_mode="HTML", reply_markup=await new_test_type())
    #     await state.set_state(PostRegistration.select_on_test_type)


async def detect_sub_fo(call: types.CallbackQuery,state:FSMContext, session_maker:sessionmaker):
    await state.update_data(test_type='90')
    datas = await get_schname_tsub(int(call.from_user.id), session_maker)

    t_subject=datas.teacher_subject
    await state.update_data(t_subject=t_subject)
    await call.message.answer(f"{t_subject} olmoqchi bo‘lgan testingiz uchun nechanchi darajali fan:",
                           reply_markup=k_select_subject_degree)
    await state.set_state(PostRegistration.detect_on_subject)
async def send_file_fo30(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Testni <a href=\"https://t.me/namuna_kana/2\">namunada</a> ko‘rsatilganidek shaklda jo‘nating va uyog‘ini bizga qo‘yib bering😊", reply_markup=back_2_menu,  cache_time=1, parse_mode="HTML", disable_web_page_preview=True)
    await state.set_state(PostRegistration.send_file_on)
    await state.update_data(test_type='30')

async def send_file_fo90(call: types.CallbackQuery, state: FSMContext):
    if call.data.startswith('sub_s_first_'):
        print('2', call.data[12:])
        await state.update_data(subject_2=call.data[12:])

    else:
        print('1', call.data[13:])
        await state.update_data(subject_1=call.data[13:])

    await call.message.answer("Testni <a href=\"https://t.me/namuna_kana/2\">namunada</a> ko‘rsatilganidek shaklda jo‘nating va uyog‘ini bizga qo‘yib bering😊", reply_markup=back_2_menu,  cache_time=1, parse_mode="HTML", disable_web_page_preview=True)
    await state.set_state(PostRegistration.send_file_on)


async def get_file_on(message: types.Message, state: FSMContext, bot: Bot, session_maker: sessionmaker):
    user_data = await state.get_data()


    test_type = user_data['test_type']

    expire_date = user_data['expire_date']
    if test_type=='90':
        second_sub = user_data['subject_1'].replace('_', ' ')

        third_sub = user_data['subject_2'].replace('_', ' ')
        print(second_sub, third_sub)
        channel_link = user_data['channel_link']

        save_to_io = BytesIO()

        await bot.download(
            message.document,
            destination=save_to_io
        )
        datas = await get_schname_tsub(int(message.from_user.id), session_maker)

        save_to_title_pdf = await create_title_on(message.from_user.id, datas.school_name, d1, channel_link,
                                                  second_sub, third_sub, test_type, None)
        document = types.input_file.BufferedInputFile(file=save_to_title_pdf, filename='@ce_test_center_bot.pdf')
        await bot.send_document(message.chat.id, document=document)
        try:
            save_to_pdf, epd = await create_pdf_on(save_to_io, test_type, second_sub, third_sub, expire_date, d1,
                                              message.from_user.id, session_maker, None, channel_link,
                                              datas.school_name)
            if epd:
                expire_date_text= f'⏰Testni tekshirish yakunlanadigan vaqt:\n<code>{epd}</code>'
            else:
                expire_date_text = f'⏰Testni tekshirish yakunlanadigan vaqt:\n<code>Belgilanmagan</code>'
            document = types.input_file.BufferedInputFile(file=save_to_pdf, filename='@ce_test_center_bot.pdf')
            await bot.send_document(message.chat.id, document=document, caption=f'📕Birinchi mutaxasislik fani:\n<code>{second_sub}</code>\n\n📗Ikkinchi mutaxasislik fani:\n<code>{third_sub}</code>\n\n🔑Test tekshirish kodi:\n<code>90{message.from_user.id}</code>\n\n{expire_date_text}\n\n📣Muallif kanali:\n{channel_link}')
            await change_is_used(message.from_user.id, session_maker)



        except IndexError as e:
            await bot.send_message(message.chat.id,
                                   f"Jo'natilgan faylda testlar soni {test_type}tadan kam, yoki testlar xato kiritilgan")
            print(e)

    else:

        channel_link = user_data['channel_link']

        save_to_io = BytesIO()

        await bot.download(
            message.document,
            destination=save_to_io
        )
        datas = await get_schname_tsub(int(message.from_user.id), session_maker)

        save_to_title_pdf = await create_title_on(message.from_user.id, datas.school_name, d1, channel_link,
                                                  None, None, test_type,datas.teacher_subject)
        document = types.input_file.BufferedInputFile(file=save_to_title_pdf, filename='@ce_test_center_bot.pdf')
        await bot.send_document(message.chat.id, document=document)
        try:
            save_to_pdf,epd = await create_pdf_on(save_to_io, test_type, None, None, expire_date, d1,
                                              message.from_user.id, session_maker, datas.teacher_subject, channel_link,
                                              datas.school_name)
            if epd:
                expire_date_text = f'⏰Testni tekshirish yakunlanadigan vaqt:\n<code>{epd}</code>'
            else:
                expire_date_text = f'⏰Testni tekshirish yakunlanadigan vaqt:\n<code>Belgilanmagan</code>'

            document = types.input_file.BufferedInputFile(file=save_to_pdf, filename='@ce_test_center_bot.pdf')
            await bot.send_document(message.chat.id, document=document,
                                    caption=f'Fan nomi:\n<code>{datas.teacher_subject}</code>\n\n🔑Test tekshirish kodi:\n<code>30{message.from_user.id}</code>\n\n{expire_date_text}\n\n📣Muallif kanali:\n{channel_link}')
            await change_is_used(message.from_user.id, session_maker)




        except IndexError as e:
            await bot.send_message(message.chat.id,
                                   f"Jo'natilgan faylda testlar soni {test_type}tadan kam, yoki testlar xato kiritilgan")
            print(e)







    await reg_menu(message, state)

async def check_online_test(message: types.Message, state: FSMContext,session_maker: sessionmaker):
    is_regisered =await is_registered(message.from_user.id, session_maker)
    if is_regisered==2:
        await message.answer('Natijani qaysi usulda tekshirishni istaysiz?', reply_markup=method_of_checking)
        await state.set_state(StudentMenu.select_m_check_online)
    elif is_regisered==1:
        await message.answer(
            '😔Afsuski, sizga berilgan barcha imkoniyatdan foydalanib bo‘lgansiz. Botdan cheklovlarsiz foydalanish uchun ustozingizga xabar bering. Ustozingiz ro‘yxatdan o‘tgan bo‘lsa, asosiy menyudan\n"Ma\'lumotlarni tahrirlash✏️"->"O‘quvchi qo‘shish➕" orqali sizni guruhga qo‘shishi, '
            'agar ro‘yxatdan o‘tmagan bo‘lsa, ro‘yxatdan o‘tish davomida sizni guruhga qo‘shishi mumkin, quyida bu bo‘yicha qo‘llanmani ko‘rsatishingiz mumkin\n\nhttps://telegra.ph/Card-ED-Test-Centerdan-royxatdan-otish-07-18'

        )
    else:
        await message.answer(
                             '😔Afsuski, siz hech qaysi guruhga qo‘shilmagansiz. Guruhga qo‘shilish uchun ustozingizga xabar bering. Ustozingiz ro‘yxatdan o‘tgan bo‘lsa, asosiy menyudan\n"Ma\'lumotlarni tahrirlash✏️"->"O‘quvchi qo‘shish➕" orqali sizni guruhga qo‘shishi, '
                             'agar ro‘yxatdan o‘tmagan bo‘lsa, ro‘yxatdan o‘tish davomida sizni guruhga qo‘shishi mumkin, quyida bu bo‘yicha qo‘llanmani ko‘rsatishingiz mumkin\nhttps://telegra.ph/Card-ED-Test-Centerdan-royxatdan-otish-07-18\n\n'
                             '<i>Xavotirlanmang, ustozingiz guruhga qo‘shgungacha siz ishlagan testingizni tekshirib turishingiz mumkin😉. Buning uchun ism-familiyangizni yozib jo‘nating.</i>'
                             )
        await state.set_state(StudentMenu.start_own_register)

async def get_fullname_fo(message:types.Message, state:FSMContext, session_maker:sessionmaker):
    await register_student_fof(message.from_user.id, message.text, session_maker)
    await message.answer('<i>Ustozingiz sizni guruhga qo‘shgunicha onlayn test tekshirish uchun sizga 5 ta imkoniyat taqdim qilamiz</i>\n\nNatijani qaysi usulda tekshirishni istaysiz?', reply_markup=method_of_checking)
    await state.set_state(StudentMenu.select_m_check_online)






async def about_OMR_checking(message: types.Message, state: FSMContext):

    await message.answer('Natijalarni tekshirish uchun titulni rasmga olib yuboring')
    await state.set_state(StudentMenu.scan_omr)


async def OMR_checking(message: types.Message, state: FSMContext, bot: Bot, session_maker:sessionmaker):
    photo_io = BytesIO()
    await bot.download(
        message.photo[-1],
        destination=photo_io
    )
    # try:
    grading = await test_scanner_fo(photo_io,message.from_user.id, session_maker )
    await message.reply(grading, parse_mode="HTML")
    await message.answer("O‘zingizga kerakli bo‘lgan menyuni tanlang", reply_markup=student_key)

    await state.set_state(Registration.show_res)
    # except:
    #     await message.reply(
    #         "<b>XATOLIK YUZ BERDI</b>\n\nTitulni yaxshiroq yorug‘likda, tepasidan to‘g‘rilab olishga harakat qiling. Agar bu ham yordam bermagan bo‘lsa, iltimos, bizga murojaat qiling",
    #         parse_mode="HTML")
    #     return



async def get_test_code(message: types.Message, state: FSMContext):
    await message.answer('Testni tekshirish uchun test kodini kiriting:', reply_markup=await back(None))
    await state.set_state(StudentMenu.get_code)
async def test_hand(message: types.Message, state: FSMContext, session_maker:sessionmaker):
    pattern = '^\d+$'
    result = re.match(pattern, message.text)
    if len(message.text)<4:
        await message.answer("Kiritilgan test kodi juda ham qisqa, iltimos, qaytadan kiriting:")
    elif result:
        can__use, data_s = await can_i_use(int(message.text[2:]), message.text[:2], session_maker)
        if not can__use:
            await message.answer(
                'Ushbu kod xato kiritilgan yoki test o‘tkazish muddati tugagan\n\n<i>Qaytadan to‘g‘risini kiriting yoki "Ortga qaytish🔙" tugmasini bosib ortga qaytishingiz mumkin</i>')
        # elif str(message.from_user.id) in data_s:
        #     await message.answer(
        #         'Bitta testni har bir abituriyent faqat bir marta ishlashi mumkin\n\n<i>Qaytadan boshqasini kiriting yoki "Ortga qaytish🔙" tugmasini bosib ortga qaytishingiz mumkin</i>')
        elif message.text[:2] == '90':

            answer_sh = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                         5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5,
                         5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
            await state.update_data(answer_sh=answer_sh, test_code=message.text)
            await state.set_state(StudentMenu.enter_test)
            await message.answer(
                'Natijani tekshirish uchun to‘g‘ri javoblarni belgilang:\n\n<i>Agar qaysidir javobni xato kiritgan bo‘lsangiz "🔁" shu belgini bosish orqali qaytadan kirishingiz mumkin</i>',
                reply_markup=await get_keyboard_fab(answer_sh, 0, int(message.text[:2])), parse_mode="HTML")

        else:
            answer_sh = [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
            await state.update_data(answer_sh=answer_sh, test_code=message.text)
            await state.set_state(StudentMenu.enter_test)

            await message.answer(
                'Natijani tekshirish uchun to‘g‘ri javoblarni belgilang:\n\n<i>Agar qaysidir javobni xato kiritgan bo‘lsangiz "🔁" shu belgini bosish orqali qaytadan kirishingiz mumkin</i>',
                reply_markup=await get_keyboard_fab(answer_sh, 0, int(message.text[:2])), parse_mode="HTML")



    else:
        await message.answer("Test kodi faqat raqamlardan iborat bo‘lishi mumkin, iltimos, qaytadan kiriting:")


async def select_role(message: types.Message, state: FSMContext):
    await message.answer("Kim sifatida davom ettirmoqchisiz", reply_markup=slct_role)
    await state.set_state(Registration.slkt_role)

async def test_fabric(call:types.CallbackQuery, callback_data:ChoosesCallbackFactory , state: FSMContext):
    user_data = await state.get_data()
    answer_sh = user_data['answer_sh']

    answer_sh[callback_data.column_n]=callback_data.row_n

    await state.update_data(answer_sh=answer_sh)
    await call.message.edit_text('Natijani tekshirish uchun to‘g‘ri javoblarni belgilang:\n\n<i>Agar qaysidir javobni xato kiritgan bo‘lsangiz "🔁" shu belgini bosish orqali qaytadan kirishingiz mumkin</i>', reply_markup=await get_keyboard_fab(answer_sh, callback_data.page_num,len(answer_sh)))
async def retry_answer(call:types.CallbackQuery, callback_data:ChoosesCallbackFactory , state: FSMContext):
    user_data = await state.get_data()
    answer_sh = user_data['answer_sh']
    answer_sh[callback_data.column_n] = 5
    await state.update_data(answer_sh=answer_sh)
    await call.message.edit_text('Natijani tekshirish uchun to‘g‘ri javoblarni belgilang:\n\n<i>Agar qaysidir javobni xato kiritgan bo‘lsangiz "🔁" shu belgini bosish orqali qaytadan kirishingiz mumkin</i>',
                                 reply_markup=await get_keyboard_fab(answer_sh, callback_data.page_num,len(answer_sh)))

async def next_page(call:types.CallbackQuery, callback_data:ChoosesCallbackFactory , state: FSMContext):
    user_data = await state.get_data()
    answer_sh = user_data['answer_sh']
    await call.message.edit_text('Natijani tekshirish uchun to‘g‘ri javoblarni belgilang:\n\n<i>Agar qaysidir javobni xato kiritgan bo‘lsangiz "🔁" shu belgini bosish orqali qaytadan kirishingiz mumkin</i>',
                                 reply_markup=await get_keyboard_fab(answer_sh, callback_data.page_num,len(answer_sh)))

async def confirm_answer(call:types.CallbackQuery, callback_data: ChoosesCallbackFactory, state: FSMContext):
    user_data = await state.get_data()
    answer_sh = user_data['answer_sh']
    choosl=['A  ','B  ','C  ','D  ','F','❗']
    is_confirmed='<b>Agar barchasi to‘g‘ri kiritilgan bo‘lsa tasdiqlash tugmasini bosing, aks holda "Ortga qaytish" tugmasini bosib qaytadan kiriting:</b>\n\n'
    qu=int(callback_data.test_type/3)
    for i in range(qu):

        is_confirmed += f"\n{i+1}. {choosl[answer_sh[i]]}  {i+qu+1}. {choosl[answer_sh[i + qu]]}  {i+qu*2+1}. {choosl[answer_sh[i + qu * 2]]}"
    await call.message.answer(is_confirmed, parse_mode="HTML", reply_markup=await confirm_or_back(callback_data.test_type, callback_data.page_num))

async def check_inline_response(call: types.CallbackQuery, callback_data: ChoosesCallbackFactory, state: FSMContext, session_maker:sessionmaker):
    user_data = await state.get_data()
    answer_sh = user_data['answer_sh']
    test_code = user_data['test_code']
    data,fullname = await get_answers_oo(int(test_code[2:]),test_code[:2], session_maker, call.from_user.id)
    if test_code[:2] == '90':
        second_s = data.subject_1
        third_s = data.subject_2
        ans = data.st_answers90
        questions = 30
    elif test_code[:2] == '30':
        ans = data.st_answers30
        questions = 10

    grading = ""
    symb = []
    ns = 1
    choos = "ABCD"
    for i in range(questions*3):
        if int(ans[i]) == answer_sh[i]+1:

            symb.append(f"{i+1}. {choos[answer_sh[i]]}✅")
            grading += str(1)

        elif answer_sh[i] == 5:
            if ns <= 9:
                symb.append(f"{i+1}.   ❗️ ")
            else:
                symb.append(f"{i+1}.  ❗️ ")
            grading += str(0)
        else:

            symb.append(f"{i+1}. {choos[answer_sh[i]]}❌")
            grading += str(0)


    firsts = grading[:questions].count('1')
    seconds = grading[questions:questions * 2].count('1')
    thirds = grading[questions * 2:questions * 3].count('1')
    if test_code[:2] == '90':
        resultg = (firsts * 1.1 + seconds * 3.1 + thirds * 2.1)
        resultg = round(resultg, 1)
        anw_message = f'{html.bold(html.quote(fullname))}\n———————————-\n<tg-spoiler>{resultg} ball</tg-spoiler>\n———————————-\n<tg-spoiler><b>Majburiy fanlar:</b> {firsts}\n<b>{second_s}:</b> {seconds}\n<b>{third_s}:</b> {thirds}</tg-spoiler>\n———————————-'
    else:

        resultg = (firsts + seconds + thirds) * 1.0
        resultg = round(resultg, 1)
        anw_message = f'{html.bold(html.quote(fullname))}\n———————————-\n<tg-spoiler>{resultg} ta to‘g‘ri</tg-spoiler>\n———————————-'

    for i in range(questions):
        anw_message += f"\n{symb[i]}  {symb[i + questions]}  {symb[i + questions * 2]}"
    datNow = datetime.datetime.now()
    await add_to_dict(int(test_code[2:]), call.from_user.id, str(resultg) + '%'+fullname+ '%'+str(datNow), session_maker)



    await call.message.answer(anw_message, reply_markup=student_key)
    await call.message.answer("O‘zingizga kerakli bo‘lgan menyuni tanlang", reply_markup=student_key)


    await state.set_state(Registration.show_res)

async def student_menu(messag: types.Message|types.CallbackQuery, state: FSMContext,bot: Bot, id: int = None):

    if not id:
        await messag.answer("O‘zingizga kerakli bo‘lgan menyuni tanlang", reply_markup=student_key)
    else:
        await bot.send_message(id,"O‘zingizga kerakli bo‘lgan menyuni tanlang", reply_markup=student_key)
    await state.set_state(Registration.show_res)


async def select_sub_name(message: types.Message,state: FSMContext,session_maker: sessionmaker,bot: Bot):


    sub_names = await get_sub_names(int(message.from_user.id), session_maker)
    print(sub_names)
    if sub_names != []:
        builder = InlineKeyboardBuilder()
        for i in sub_names:
            builder.add(types.InlineKeyboardButton(text=i.t_fullname, callback_data=f'sub_{i.teacher_id}'))
            print(i.teacher_id)
        builder.adjust(1)

        await message.answer("Qaysi ustoz olgan test natijasini ko‘rishni istaysiz?",reply_markup=builder.as_markup())
    else:
        await message.answer('Siz hech qaysi guruhga qo‘shilmagansiz. Guruhga qo‘shilish uchun ustozingizga xabar bering. Ustozingiz ro‘yxatdan o‘tgan bo‘lsa, asosiy menyudan\n"Ma\'lumotlarni tahrirlash✏️"->"O‘quvchi qo‘shish➕" orqali sizni guruhga qo‘shishi, '
                             'agar ro‘yxatdan o‘tmagan bo‘lsa, ro‘yxatdan o‘tish davomida sizni guruhga qo‘shishi mumkin, quyida bu bo‘yicha qo‘llanmani ko‘rsatishingiz mumkin:\nhttps://telegra.ph/Card-ED-Test-Centerdan-royxatdan-otish-07-18')
        await student_menu(message, state, bot)
async def result_msg(call: types.CallbackQuery, state: FSMContext,bot:Bot, session_maker: sessionmaker):

    result = await get_ans_message(call.from_user.id,call.data[4:], session_maker)
    print(result)
    await call.message.answer(result.replace('%^', "\n"), parse_mode="HTML")
    await student_menu(call, state, bot, call.from_user.id)
async def tutorial(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    await wr_starter_db(message.from_user.id, session_maker, message.from_user.full_name, message.from_user.username)

    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}, boshlashdan oldin iltimos qo‘llanma bilan yaxshilab tanishib chiqing: \n https://telegra.ph/Card-ED-Test-Centerdan-royxatdan-otish-07-18", reply_markup=clear)
    await state.set_state(Registration.tutorial)
    #await state.set_state(PostRegistration.menu)

async def register_t_name(message: types.Message, state: FSMContext):
    await message.answer(f"Ism-familiyangiz rostdan {message.from_user.full_name}mi?\n\nAgar ism-familiyangiz to‘g‘ri bo‘lsa pastdagi 'Ha' tugmasini bosing, aks holda to‘g‘ri ism-famiiyani yozib jo‘nating", reply_markup=yes)
    await state.set_state(Registration.register_t_name)

async def register_school_name(message: types.Message, state: FSMContext,  bot: Bot):
    try:
        if message.text == "Ha":
            t_name = message.from_user.full_name
            await state.update_data(t_name=t_name)
            t_id = message.from_user.id
            await state.update_data(t_id=t_id)

        else:
            t_name = message.text
            await state.update_data(t_name=t_name)
            t_id = message.from_user.id
            await state.update_data(t_id=t_id)
        useid = message.from_user.id
    except:
        user_data = await state.get_data()
        t_name = user_data['t_name']
        user_data = await state.get_data()
        useid = user_data['t_id']







    await bot.send_message(useid,f"👤<b>ISM FAMILIYA:</b> {html.italic(html.quote(t_name))}\n\nAgar ism familiyangizda xatolik bo'lsa \"Ortga qaytish🔙\" tugmasini bosib qaytadan yozib jo‘nating", parse_mode="HTML")
    await bot.send_message(useid,f"🏫O'quv muassasasi nomini yozib jo‘nating:", reply_markup=await back('TTA akademik litseyi'))
    await state.set_state(Registration.register_school_name)


async def register_region(message: types.Message, state: FSMContext,  bot: Bot):
    user_data = await state.get_data()
    useid = user_data['t_id']
    t_name = user_data['t_name']
    try:
        scname = message.text
        await state.update_data(sc_name=scname)
    except:
        scname = user_data['sc_name']

    await bot.send_message(useid,f'👤<b>ISM FAMILIYA:</b> {html.italic(html.quote(t_name))}\n🏫<b>O‘QUV MUASSASASI NOMI:</b> {html.italic(html.quote(scname))}\n\n--------------------\n\n<i>Agar yuqoridagi ma’lumotlarda xatolik bo‘lsa \"Ortga qaytish🔙\" tugmasini bosib qaytadan jo‘natishingiz mumkin</i>\n\n', parse_mode="HTML")
    await bot.send_message(useid,'🗺O‘quv muassasasi joylashgan hududni tanlang:',reply_markup=k_regions)
async def register_district(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(region=call.data[7:])
    user_data = await state.get_data()
    t_name = user_data['t_name']
    scname = user_data['sc_name']
    if call.data == 'region_Andijon viloyati':
        key_var = k_andijon
    elif call.data == 'region_Buxoro viloyati':
        key_var = k_bukhara
    elif call.data == 'region_Fargʻona viloyati':
        key_var = k_fergana
    elif call.data == 'region_Jizzax viloyati':
        key_var = k_jizzakh
    elif call.data == 'region_Xorazm viloyati':
        key_var = k_xorazm
    elif call.data == 'region_Namangan viloyati':
        key_var = k_namangan
    elif call.data == 'region_Navoiy viloyati':
        key_var = k_A_NAVOIY
    elif call.data == 'region_Qashqadaryo viloyati':
        key_var = k_qashqadaryo
    elif call.data == 'region_Qoraqalpogʻiston Respublikasi':
        key_var = k_karakalpak
    elif call.data == 'region_Samarqand viloyati':
        key_var = k_samarkand
    elif call.data == 'region_Sirdaryo viloyati':
        key_var = k_sirdaryo
    elif call.data == 'region_Surxondaryo viloyati':
        key_var = k_surxondaryo
    elif call.data == 'region_Toshkent viloyati':
        key_var = k_tashkent_reg
    elif call.data == 'region_Toshkent shahri':
        key_var = k_tashkent_city


    await call.message.edit_text(f'👤<b>ISM FAMILIYA:</b> {html.italic(html.quote(t_name))}\n🏫<b>O‘QUV MUASSASASI NOMI:</b> {html.italic(html.quote(scname))}\n<b>🗺HUDUD:</b> <i>{call.data[7:]}</i>\n\n--------------------\n\n<i>Agar yuqoridagi ma’lumotlarda xatolik bo‘lsa \"Ortga qaytish🔙\" tugmasini bosib qaytadan jo‘natishingiz mumkin</i>\n\n🏙O‘quv muassasasi joylashgan tumanni tanlang:', reply_markup=key_var, parse_mode="HTML")




async def register_subject(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    scname = user_data['sc_name']
    useid = user_data['t_id']
    region = user_data['region']
    t_name = user_data['t_name']




    await state.update_data(students_id=[], students_name=[])
    try:
        await state.update_data(district=call.data[9:])
        district = call.data[9:]
    except:
        district = user_data['district']







    await bot.send_message(useid,f"👤<b>ISM FAMILIYA:</b> {html.italic(html.quote(t_name))}\n🏫<b>O‘QUV MUASSASASI NOMI:</b> {html.italic(html.quote(scname))}\n🗺<b>HUDUD:</b> <i>{region}</i>\n🏙<b>TUMAN:</b> {district}\n\n--------------------\n\n<i>Agar yuqoridagi ma’lumotlarda xatolik bo‘lsa \"Ortga qaytish🔙\" tugmasini bosib qaytadan jo‘natishingiz mumkin</i>\n\n", parse_mode="HTML")

    await bot.send_message(useid,f"Pastdan o‘zingiz dars beradigan fanni tanlang:", reply_markup=keyboard)
    await state.set_state(Registration.register_subject)

async def register_group_name(call: types.CallbackQuery,state: FSMContext):
    user_data = await state.get_data()
    scname = user_data['sc_name']
    useid = user_data['t_id']
    region = user_data['region']
    district = user_data['district']
    t_name = user_data['t_name']
    if call.data == 'detect_back':
        t_subject = user_data['t_subject']
    else:
        await state.update_data(t_subject=call.data[5:].replace('_',' '))
        t_subject = call.data[5:].replace('_',' ')
    await call.message.answer(f"👤<b>ISM FAMILIYA:</b> {html.italic(html.quote(t_name))}\n"
                              f"🏫<b>O‘QUV MUASSASASI NOMI:</b> {html.italic(html.quote(scname))}\n"
                              f"🗺<b>HUDUD:</b> <i>{region}</i>\n🏙<b>TUMAN:</b> {district}\n"
                              f"📚<b>FAN:</b> <i>{t_subject}</i>\n\n"
                              f"--------------------\n\n"
                              f"<i>Agar yuqoridagi ma’lumotlarda xatolik bo‘lsa \"Ortga qaytish🔙\" tugmasini bosib qaytadan jo‘natishingiz mumkin</i>\n\n", parse_mode="HTML")
    await call.message.answer(
        f"Dars beradigan guruhingiz nomini kiriting:",
        reply_markup=await back('20-02'))
    await state.set_state(Registration.register_group_name)

async def register_new_group_name(message: types.Message|types.CallbackQuery, state: FSMContext, session_maker: sessionmaker, bot: Bot) :


    try:
        uid = message.from_user.id
    except:
        uid = message.data.id
    groups = await get_group_names(uid, session_maker)
    is_premium = await premium_checker(uid, session_maker)
    if len(groups)==2 and is_premium == False:
        await bot.send_message(uid,'Siz bepul tarifdasiz! Shu sababli Premium tarif rasmiylashtirmaguningizgacha 2 tadan ko‘p guruh qo‘sha olmaysiz.\n\n'
                                   'Premium tarif rasmiylashtirganingizdan so‘ng siz imkoniyatlaringizni ikki barobar ko‘paytirasiz, ya\'ni 4 tagacha guruh, har bir guruhga 30 tagacha odam qo‘shish, <b>onlayn test o‘tkazish</b> imkoniyatiga ega bo‘lasiz '
                                   'va <b>eng asosiysi loyihani davom etishi va siz uchun yangidan-yangi imkoniyatlar yaratishimiz uchun katta yordam berasiz</b>\n\n'
                                   '<i>Quyida kerakli tarifni tanlab, Click to‘lov tizimi orqali to‘lovni amalga oshirishingiz mumkin</i>' , parse_mode="HTML"
                                  )
        await bot.send_invoice(
            chat_id=uid,
            title='30 kunlik Premiumni sotib olish',
            description='Premiumni rasmiylashtirish uchun karta ma\'lumotlaringizni kiriting ',
            payload='premium30',
            provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065',
            currency='UZS',
            prices=[
                types.LabeledPrice(
                    label="Premium tarifi",
                    amount=2000000
                )
            ],
            need_name=True

        )
    elif len(groups)==4:
        await bot.send_message(uid,'4 tadan ko‘p guruh qo‘shish mumkin emas. Agar sizga bu muhim bo‘lsa, iltimos, bizga murojaat qiling.')
    elif is_premium == True:
        await bot.send_message(uid,'Yangi guruh nomini kiriting:'
                                   , reply_markup=await back('20-02'))
        tsub = await get_t_sub(uid, session_maker)

        await state.update_data(t_subject=tsub, user_id=uid)
        await state.set_state(PostRegistration.new_gr)
    elif len(groups)<2:
        await bot.send_message(uid,'Yangi guruh nomini kiriting:', reply_markup=await back('20-02'))
        tsub = await get_t_sub(uid, session_maker)

        await state.update_data(t_subject=tsub, user_id=uid)
        await state.set_state(PostRegistration.new_gr)




async def detect_subject(message: types.Message,state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    t_subject = user_data['t_subject']
    scname = user_data['sc_name']
    useid = user_data['t_id']
    region = user_data['region']
    district = user_data['district']
    t_name = user_data['t_name']
    try:
        if message.text != 'Ortga qaytish🔙':
            await state.update_data(group_name=message.text)
            group_name = message.text
        else:
            group_name = user_data['group_name']



    except:
        group_name = user_data['group_name']
    await bot.send_message(useid,f"👤<b>ISM FAMILIYA:</b> {html.italic(html.quote(t_name))}\n"
                              f"🏫<b>O‘QUV MUASSASASI NOMI:</b> {html.italic(html.quote(scname))}\n"
                              f"🗺<b>HUDUD:</b> <i>{region}</i>\n🏙<b>TUMAN:</b> {district}\n"
                              f"📚<b>FAN:</b> <i>{t_subject}</i>\n"
                                   f"👥<b>GURUH NOMI:</b> {html.italic(html.quote(group_name))}\n\n"
                              f"--------------------\n\n"
                              f"<i>Agar yuqoridagi ma’lumotlarda xatolik bo‘lsa \"Ortga qaytish🔙\" tugmasini bosib qaytadan jo‘natishingiz mumkin</i>\n\n", parse_mode="HTML")


    await bot.send_message(useid,
        f"{t_subject} kiritgan guruhingiz uchun nechanchi darajali fan:",
        reply_markup=k_select_subject_degree)



async def new_detect_subject(message: types.Message|types.CallbackQuery,state: FSMContext, bot: Bot, session_maker: sessionmaker):
    user_data = await state.get_data()
    t_subject = user_data['t_subject']

    try:

        id = user_data['user_id']
        groups = await get_group_names(id, session_maker)
        if message.text != "Ortga qaytish🔙" and message.text not in groups:
            await state.update_data(group_name=message.text)

            t_subject = user_data['t_subject']



            await bot.send_message(id,
                                   f"{t_subject} kiritgan guruhingiz uchun nechanchi darajali fan:",
                                   reply_markup=k_select_subject_degree)
        elif message.text in groups:
            await bot.send_message(id, 'Yangi guruh nomi oldingilari bilan bir xil bo‘lmasligi kerak. \n\n<i>Iltimos, qaytadan boshqacharoq nom yozib ko‘ring</i>', parse_mode='HTML')
    except:
        await bot.send_message(message.from_user.id,
                               f"{t_subject} kiritgan guruhingiz uchun nechanchi darajali fan:",
                               reply_markup=k_select_subject_degree)
    await state.set_state(PostRegistration.post_new_gr)

async def select_subject(call: types.CallbackQuery,state: FSMContext):
    user_data = await state.get_data()
    subject_name = user_data['t_subject']
    state_name = await state.get_state()
    if call.data == "first_subject":
        await state.update_data(subject_1=subject_name)
        daraja = '📗Kiritgan guruhingiz uchun ikkinchi'
        if state_name=='PostRegistration:detect_on_subject':
            daraja = '📗Olmoqchi bo‘lgan testingiz uchun ikkinchi'
        if subject_name == "Biologiya":
            key_subject = k_first_biology
        elif subject_name == 'Fizika':
            key_subject = k_first_physics
        elif subject_name == 'Kimyo':
            key_subject = k_first_chemistry
        elif subject_name == 'Ingliz tili':
            key_subject = k_first_english
        elif subject_name == 'Fransuz tili':
            key_subject = k_first_french
        elif subject_name == 'Tarix':
            key_subject = k_first_history
        elif subject_name == 'Nemis tili':
            key_subject = k_first_deutsch
        elif subject_name == 'Rus tili va adabiyoti':
            key_subject = k_first_russian
        elif subject_name == 'Ona tili va adabiyoti':
            key_subject = k_first_mother_t
        elif subject_name == 'Geografiya':
            key_subject = k_first_geography
        elif subject_name == 'Matematika':
            key_subject = k_first_math
        elif subject_name == 'Qoraqalpoq tili va adabiyoti':
            key_subject = k_first_karakalpak



    else:
        await state.update_data(subject_2=subject_name)
        daraja = '📕Kiritgan guruhingiz uchun birinchi'
        if state_name=='PostRegistration:detect_on_subject':
            daraja = '📗Olmoqchi bo‘lgan testingiz uchun birinchi'
        if subject_name == "Biologiya":
            key_subject = k_second_biology
        elif subject_name == 'Fizika':
            key_subject = k_second_physics
        elif subject_name == 'Kimyo':
            key_subject = k_second_chemistry
        elif subject_name == 'Ingliz tili':
            key_subject = k_second_english
        elif subject_name == 'Fransuz tili':
            key_subject = k_second_french
        elif subject_name == 'Tarix':
            key_subject = k_second_history
        elif subject_name == 'Nemis tili':
            key_subject = k_second_deutsch
        elif subject_name == 'Rus tili va adabiyoti':
            key_subject = k_second_russian
        elif subject_name == 'Ona tili va adabiyoti':
            key_subject = k_second_mother_t
        elif subject_name == 'Geografiya':
            key_subject = k_second_geography
        elif subject_name == 'Matematika':
            key_subject = k_second_math
        elif subject_name == 'Qoraqalpoq tili va adabiyoti':
            key_subject = k_second_karakalpak

    await call.message.answer(f'{daraja} darajali fannni tanlang:', reply_markup=key_subject)



async def about_register_students(call: types.CallbackQuery,state: FSMContext, bot:Bot):
    user_data = await state.get_data()
    t_subject = user_data['t_subject']
    scname = user_data['sc_name']
    useid = user_data['t_id']
    region = user_data['region']
    district = user_data['district']
    t_name = user_data['t_name']
    group_name = user_data['group_name']
    if call.data.startswith('sub_s_first_'):
        print('2',call.data[12:])
        await state.update_data(subject_2=call.data[12:])
        subject_2 = call.data[12:]
        subject_1 = t_subject
    else:
        print('1',call.data[13:])
        await state.update_data(subject_1=call.data[13:])
        subject_1 = call.data[13:]
        subject_2 = t_subject
    await call.message.answer( f"👤<b>ISM FAMILIYA:</b> {html.italic(html.quote(t_name))}\n"
                                  f"🏫<b>O‘QUV MUASSASASI NOMI:</b> {html.italic(html.quote(scname))}\n"
                                  f"🗺<b>HUDUD:</b> <i>{region}</i>\n🏙<b>TUMAN:</b> {district}\n"
                                  f"📚<b>FAN:</b> <i>{t_subject}</i>\n"
                                  f"👥<b>GURUH NOMI:</b> {html.italic(html.quote(group_name))}\n"
                               f"📕<b>BIRINCHI DARAJALI FAN:</b> <i>{subject_1}</i>\n"
                               f"📗<b>IKKINCHI DARAJALI FAN:</b> <i>{subject_2}</i>\n\n"
                                  f"--------------------\n\n"
                                  f"<i>Agar yuqoridagi ma’lumotlarda xatolik bo‘lsa \"Ortga qaytish🔙\" tugmasini bosib qaytadan jo‘natishingiz mumkin</i>\n\n",
                           parse_mode="HTML")

    await bot.send_animation(call.from_user.id,
                             'CgACAgIAAxkBAAIXKmShmmM8ixMcRjaqoKbVuPOI1_WPAAIXMAAC3b4QSW2R36HUv-pWLwQ',
                             caption=f"O‘quvchini qo‘shish uchun uning ism-familiyasi yozilgan xabarini botga uzating (\"Переслать\" qiling)\n\nQo‘shib bo‘lganingizdan so'ng \"Qo‘shishni yakunlash\" tugmasini bosing", reply_markup=end)

    print(call.data[:7])

    await state.update_data(subject=call.data[5:], cou=[])
    await state.set_state(Registration.register_students)

async def new_about_register_st(call: types.CallbackQuery,state: FSMContext, bot:Bot):

    if call.data.startswith('sub_s_first_'):
        print('2',call.data[12:])
        await state.update_data(subject_2=call.data[12:])

    else:
        print('1',call.data[13:])
        await state.update_data(subject_1=call.data[13:])

    await bot.send_animation(call.from_user.id,
                             'CgACAgIAAxkBAAIXKmShmmM8ixMcRjaqoKbVuPOI1_WPAAIXMAAC3b4QSW2R36HUv-pWLwQ',
                             caption=f"O‘quvchini qo‘shish uchun uning ism-familiyasi yozilgan xabarini botga uzating (\"Переслать\" qiling)\n\nQo‘shib bo‘lganingizdan so'ng \"Qo‘shishni yakunlash\" tugmasini bosing",reply_markup=nend)
    await state.update_data(students_id=[], students_name=[], cou =[])
    await state.set_state(PostRegistration.register_students_new)
async def about_delete_students(message: types.Message,state:FSMContext):
    await message.reply(f"O‘quvchini o‘chirish uchun uning <code>TASDIQLAYMAN</code> deb yozilgan xabarini botga uzating\n\nO‘chirib bo‘lganingizdan so'ng \"O‘chirishni yakunlash\" tugmasini bosing",reply_markup=del_end,parse_mode="HTML")
    await state.set_state(PostRegistration.delete_students)
async def delete_students(message: types.Message, state: FSMContext, session_maker:sessionmaker):
    if message.forward_from and message.text == 'TASDIQLAYMAN':

        await delete_student_r(message.forward_from.id, message.from_user.id, session_maker)
        await message.reply(f"O‘quvchi muvaffaqiyatli o‘chirildi")
    elif message.forward_from:
        await message.reply(f"Xabarda faqat TASDIQLAYMAN degan yozuv bo‘lishi kerak")
    elif not message.forward_from:
        await message.reply(f"O‘quvchi tomonidan ma'lumotlari berkitilgan")



async def register_students(message: types.Message, state: FSMContext, session_maker: sessionmaker):

    user_data = await state.get_data()
    students_id=user_data['students_id']

    students_name =user_data['students_name']
    state_name = await state.get_state()
    group_name = user_data['group_name']
    cou=user_data['cou']
    is_premium = await premium_checker(message.from_user.id, session_maker)

    print(cou)


    if (message.forward_from and message.forward_from.id in students_id) or (message.forward_from and message.forward_from.id in cou):
        await message.reply(f"Ushbu o‘quvchi avval ro‘yxatga olingan")


    elif message.forward_from and len(students_name)>=(15-len(cou)) and is_premium == False:
        await message.answer_invoice(
            title='30 kunlik Premiumni sotib olish',
            description='Premiumni rasmiylashtirish uchun karta ma\'lumotlaringizni kiriting ',
            payload='premium30',
            provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065',
            currency='UZS',
            prices=[
                types.LabeledPrice(
                    label="30 kunlik Premium tarifi",
                    amount=2000000
                )
            ],
            need_name=True

        )
        await message.answer_invoice(
            title='1 kunlik Premiumni sotib olish',
            description='Premiumni rasmiylashtirish uchun karta ma\'lumotlaringizni kiriting ',
            payload='premium1',
            provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065',
            currency='UZS',
            prices=[
                types.LabeledPrice(
                    label="1 kunlik Premium tarifi",
                    amount=500000
                )
            ],
            need_name=True

        )
    elif message.forward_from and len(students_name)>=(30-len(cou)):
        await message.reply('30 tadan ko‘p o‘quvchi qo‘shish mukin emas')



    elif message.forward_from and message.forward_from.is_bot == False:
        students_id.append(message.forward_from.id)
        students_name.append(message.text)
        await state.update_data(students_id=students_id, students_name=students_name)
        await message.reply(f"O'quvchi ro'yxatga olindi")
        

        print(message.forward_from)
    elif message.text == "Ortga qaytish🔙" and state_name =="Registration:end":
        await message.answer_animation(
                                 'CgACAgIAAxkBAAIXKmShmmM8ixMcRjaqoKbVuPOI1_WPAAIXMAAC3b4QSW2R36HUv-pWLwQ',
                                 caption=f"O‘quvchini qo‘shish uchun uning ism-familiyasi yozilgan xabarini botga uzating (\"Переслать\" qiling)\n\nQo‘shib bo‘lganingizdan so'ng \"Qo‘shishni yakunlash\" tugmasini bosing", reply_markup=end)
        await state.set_state(Registration.register_students)
    elif message.text == "Ortga qaytish🔙" and state_name =="PostRegistration:add_students":
        await edit_datas(message, state, session_maker)

    elif message.text == "Ortga qaytish🔙" and state_name =="PostRegistration:register_students_new":
        await new_detect_subject(message, state, bot)

    elif not message.forward_from:
        await message.reply(f"O‘quvchi tomonidan ma'lumotlari berkitilgan")








async def pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

async def successful_payment(message: types.Message,state: FSMContext, session_maker: sessionmaker, bot: Bot):
    if message.successful_payment.invoice_payload == 'premium30':

        expire_dat=await expire_date(message.from_user.id, 30,session_maker)

        msg=await message.answer(f'Muvaffaqiyatli to‘lov qilindi! Endi 30 kun davomida 30 tagacha o‘quvchidan iborat 4 tagacha guruh bilan ishlashingiz va bot yordamida onlayn test o‘tkazishingiz mumkin. Bizni qo‘llab-quvvatlaganingiz uchun rahmat❤️\n\nAgar guruh nomini kiritayotganingizda yoki o‘quvchi habarini jo‘natayotgan paytingiz to‘lovni amalga oshirgan '
                             f'bo‘lsangiz, iltimos, guruh nomini qaytadan yozing yoki o‘quchi habarini qaytadan jo‘nating.\n\n'
                             f'Agar guruh tanlayotganingizda to‘lagan bo‘lsangiz, iltimos,  "Qaytadan tanlash🔁" tugmasini bosib shu guruhni qaytadan tanlang.\n\n\n'
                             f'<b>Premium obunani amal qilish muddati:</b> \n<code>{expire_dat}</code>', parse_mode="HTML")
        await bot.pin_chat_message(message.from_user.id, msg.message_id)
    elif message.successful_payment.invoice_payload == 'premium1':
        expire_dat = await expire_date(message.from_user.id, 1, session_maker)

        msg = await message.answer(
            f'Muvaffaqiyatli to‘lov qilindi! Endi 1 kun davomida 30 tagacha o‘quvchidan iborat 4 tagacha guruh bilan ishlashingiz va bot yordamida onlayn test o‘tkazishingiz mumkin. Bizni qo‘llab-quvvatlaganingiz uchun rahmat❤️\n\nAgar guruh nomini kiritayotganingizda yoki o‘quvchi habarini jo‘natayotgan paytingiz to‘lovni amalga oshirgan '
            f'bo‘lsangiz, iltimos, guruh nomini qaytadan yozing yoki o‘quchi habarini qaytadan jo‘nating.\n\n'
            f'Agar guruh tanlayotganingizda to‘lagan bo‘lsangiz, iltimos,  "Qaytadan tanlash🔁" tugmasini bosib shu guruhni qaytadan tanlang.\n\n\n'
            f'<b>Premium obunani amal qilish muddati:</b> \n<code>{expire_dat}</code>', parse_mode="HTML")
        await bot.pin_chat_message(message.from_user.id, msg.message_id)



async def remove_from_premium(message: types.Message, session_maker: sessionmaker,bot: Bot):
    non_premiums = await get_expired_users(session_maker)
    if non_premiums != None:
        for np in non_premiums:

            msg=await bot.send_message(np, 'Afsuski, Premium tarifi muddatingiz yakunlandi. 2 ta guruhdagi 15 tadan tashqari barcha o‘quvchilar ma\'lumotlari inaktiv holatga o‘tadi va ulardan foydalana olmaysiz. '
                                       f'O‘quvchilar ma\'lumotlarini aktiv holatga o‘tkazib undan foydalanish uchun yana Premium tarifini faollashtirishingiz kerak. '
                ' <b>Unutmang, Premiumni aktivlashtirib siz eng asosiysi loyihani davom etishi va siz uchun yangidan-yangi imkoniyatlar yaratishimiz uchun katta yordam bergan bo‘lasiz. Bizni qo‘llab-quvvatlayotganingiz uchun rahmat❤️</b>\n\n'
                '<i>Quyida kerakli tarifni tanlab, Click to‘lov tizimi orqali to‘lovni amalga oshirishingiz mumkin👇</i>',)






            await bot.send_invoice(np,title='30 kunlik Premiumni sotib olish',
                                              description='Premiumni rasmiylashtirish uchun karta ma\'lumotlaringizni kiriting ',
                                              payload='premium30',
                                              provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065',
                                              currency='UZS',
                                              prices=[
                                                  types.LabeledPrice(
                                                      label="Premium tarifi",
                                                      amount=2000000
                                                  )
                                              ],
                                              need_name=True)
            await bot.pin_chat_message(np, msg.message_id)

# async def add_new_group(message: types.Message, state: FSMContext):

async def registered_menu(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    user_data = await state.get_data()
    students_id = user_data['students_id']
    students_name = user_data['students_name']
    t_name = user_data['t_name']
    t_subject = user_data['t_subject']
    sch_name = user_data['sc_name']
    subject_1 = user_data['subject_1']
    subject_2 = user_data['subject_2']
    district = user_data['district']
    region = user_data['region']
    group_name = user_data['group_name']
    if len(students_id)>0:
        try:
            for st_id, st_name in zip(students_id, students_name):
                await create_user(st_id, message.from_user.id, st_name, t_name, t_subject, sch_name, subject_1,
                                  subject_2, district, region, group_name, session_maker)
        except (ValueError):
            await create_user(students_id[0], message.from_user.id, students_name[0], t_name, t_subject, sch_name,
                              subject_1, subject_2, district, region, group_name, session_maker)
        await message.answer(f'Ro‘yxatdan o‘tish muvaffaqiyatli yakunlandi. Telegram-botimizdan foydalanishni boshlash uchun "Davom etish⏩" tugmasini bosing', reply_markup=end_register)

        await state.set_state(Registration.end)
    else:
        await message.answer(f'Bironta ham o‘quvchi qo‘shilmagan, iltimos, qaytadan qo‘shing', reply_markup=end)



#
async def reg_menu(message: types.Message, state: FSMContext):
    await message.answer(f'Kerakli bo‘limni tanlang', reply_markup=menu)
    await state.clear()
    await state.set_state(PostRegistration.menu)

async def get_file(message: types.Message, state: FSMContext, bot: Bot, session_maker: sessionmaker):
    user_data = await state.get_data()
    groupn = user_data['groupn']
    test_type = user_data['test_type']
    book_type = user_data['bok_type']
    save_to_io = BytesIO()
    save_to_pdf = BytesIO()
    save_to_title_pdf = BytesIO()
    await bot.download(
        message.document,
        destination=save_to_io
    )
    ids = await get_st_ids(int(message.from_user.id),groupn, session_maker)
    datas = await get_st_datas(int(message.from_user.id), groupn,session_maker)
    save_to_title_pdf=await create_title(ids, message.from_user.id, datas.school_name, d1, groupn,
                 datas.subject_1.replace('_', ' '), datas.subject_2.replace('_', ' '),test_type, session_maker, datas.teacher_subject)
    document = types.input_file.BufferedInputFile(file=save_to_title_pdf, filename='@ce_test_center_bot.pdf')
    await bot.send_document(message.chat.id, document=document)
    try:
        save_to_pdf, cvl,ivl = await create_pdf(save_to_io, test_type, datas.subject_1.replace('_', ' '), datas.subject_2.replace('_', ' '), datas.school_name, ids,
                                       d1, message.from_user.id, session_maker, datas.teacher_subject, book_type)
        document = types.input_file.BufferedInputFile(file=save_to_pdf, filename='@ce_test_center_bot.pdf')
        await bot.send_document(message.chat.id, document=document)
        if cvl != 'over':
            await bot.send_message(message.chat.id,f'<b>Birinchi tarafi uchun:</b>\n\n<code>{cvl}</code>\n\n\n<b>Ikkinchi tarafi uchun: </b>\n\n<code>{ivl}</code>', parse_mode="HTML")

    except IndexError as e:
        await bot.send_message(message.chat.id,f"Jo'natilgan faylda testlar soni {test_type}tadan kam, yoki testlar xato kiritilgan")
        print(e)


    # await state.update_data(checked_status=True)
    await reg_menu(message, state)

    # await message.answer_document(types.BufferedInputFile(file=save_to_io, filename='fdf.pdf'))

    # save_to_io.close()
    # save_to_pdf.close()
async def about_scan_test(message: types.Message, state: FSMContext):
    await message.answer('Natijalarni tekshirish uchun titulni rasmga olib yuboring', reply_markup=back_2_menu)
    await state.set_state(PostRegistration.scan_test)

async def scan_test(message: types.Message, state: FSMContext, bot: Bot,session_maker: sessionmaker):
    # await asyncio.sleep(20)
    photo_io = BytesIO()
    await bot.download(
        message.photo[-1],
        destination=photo_io
    )
    try:
        grading = await test_scanner_func(photo_io,session_maker, message.from_user.id)
    except:
        await message.reply("<b>XATOLIK YUZ BERDI</b>\n\nTitulni yaxshiroq yorug‘likda, tepasidan to‘g‘rilab olishga harakat qiling. Agar bu ham yordam bermagan bo‘lsa, iltimos, bizga murojaat qiling", parse_mode="HTML")
        return

    await message.reply(grading, parse_mode="HTML")


async def select_group_name(message: types.Message,state: FSMContext,session_maker: sessionmaker):
    if message.text == 'Statistika📊':
        await state.set_state(PostRegistration.stats)
    builder = InlineKeyboardBuilder()
    group_names = await get_group_names(int(message.from_user.id), session_maker)
    for i in group_names:
        builder.add(types.InlineKeyboardButton(text=i, callback_data=f'gr_{i}'))
    builder.adjust(1)

    await message.answer("Guruhni tanlang:",reply_markup=builder.as_markup())
async def select_group_name_callback(call: types.CallbackQuery, session_maker: sessionmaker):
    builder = InlineKeyboardBuilder()
    group_names = await get_group_names(call.from_user.id, session_maker)

    for i in group_names:
        builder.add(types.InlineKeyboardButton(text=i, callback_data=f'gr_{i}'))
    builder.adjust(1)

    await call.message.answer("Guruhni tanlang:", reply_markup=builder.as_markup(),  cache_time=1)
async def select_test_type(call: types.CallbackQuery, state: FSMContext, session_maker: sessionmaker):
    await state.update_data(groupn=call.data[3:])
    bool=await is_group_active(call.from_user.id, call.data[3:], session_maker)
    print(bool)
    if bool:
        await call.message.edit_text('Test shaklini tanlang:', reply_markup=test_type,  cache_time=1)
    else:
        await call.message.edit_text(f'{call.data[3:]} ushbu guruh Premium tarifi muddati tugagani uchun inaktiv holatga o‘tkazilgan.\n\n'
                                     f' Guruhni aktiv holatga o‘tkazib undan foydalanish  uchun yana Premium tarifini faollashtirishingiz kerak. '
                                     ' <b>Unutmang, Premiumni aktivlashtirib siz eng asosiysi loyihani davom etishi va siz uchun yangidan-yangi imkoniyatlar yaratishimiz uchun katta yordam bergan bo‘lasiz. Bizni qo‘llab-quvvatlayotganingiz uchun rahmat❤️</b>\n\n'
                                     '<i>Quyida kerakli tarifni tanlab, Click to‘lov tizimi orqali to‘lovni amalga oshirishingiz mumkin👇</i>',
                                     parse_mode="HTML"
                                     )

        await call.message.answer_invoice(title='30 kunlik Premiumni sotib olish',
            description='Premiumni rasmiylashtirish uchun karta ma\'lumotlaringizni kiriting ',
            payload='premium30',
            provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065',
            currency='UZS',
            prices=[
                types.LabeledPrice(
                    label="Premium tarifi",
                    amount=2000000
                )
            ],
            need_name=True)

        await call.message.answer(
            f'Agar boshqa guruh tanlamoqchi bo‘lsangiz "Qaytadan tanlash🔁" tugmasini bosib o‘zgartirishingiz mumkin', reply_markup=re_choose_gr
           )

async def select_book_type(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(test_type=call.data[-2:])
    if call.data[-2:] == '90':
        await call.message.answer_photo('AgACAgIAAxkBAAIx1mSz0U8RFOh8t3f6E5L55Jti9u00AAIB4TEb92WgSfJBToXLfEjCAQADAgADeQADLwQ',caption='Test kitobchasi shaklini tanlang:', reply_markup=k_select_book_type,  cache_time=1)
    else:
        await call.message.answer_photo('AgACAgIAAxkBAAIx1mSz0U8RFOh8t3f6E5L55Jti9u00AAIB4TEb92WgSfJBToXLfEjCAQADAgADeQADLwQ',caption='Test kitobchasi shaklini tanlang:', reply_markup=k_select_book_type30,  cache_time=1)
async def send_file(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Testni <a href=\"https://t.me/namuna_kana/2\">namunada</a> ko‘rsatilganidek shaklda jo‘nating va uyog‘ini bizga qo‘yib bering😊", reply_markup=back_2_menu,  cache_time=1, parse_mode="HTML", disable_web_page_preview=True)
    await state.set_state(PostRegistration.send_file)
    await state.update_data(bok_type=call.data[5:])

async def send_file30(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Testni <a href=\"https://t.me/namuna_kana/2\">namunada</a> ko‘rsatilganidek shaklda jo‘nating va uyog‘ini bizga qo‘yib bering😊", reply_markup=back_2_menu,  cache_time=1, parse_mode="HTML", disable_web_page_preview=True)
    await state.set_state(PostRegistration.send_file)
    await state.update_data(bok_type=call.data[7:])



async def callback_back(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    if call.data == 'district_back':
        await register_region(types.Message,state=state)
    elif call.data == 'select_back':
        await new_detect_subject(call, state, bot)



async def edit_datas(message: types.Message, state: FSMContext,session_maker: sessionmaker):
    state_name = await state.get_state()



    await message.answer('O‘zgartirish uchun ma\'lumotni tanlang', reply_markup=edit_menu)
    if state_name == 'PostRegistration:add_students' or state_name == 'PostRegistration:register_students_new':
        try:
            user_data = await state.get_data()
            students_id = user_data['students_id']
            print(students_id)
            if len(students_id) > 0:
                group_name = user_data['group_name']
                if state_name == 'PostRegistration:add_students':
                    data = await get_st_dats(message.from_user.id, session_maker, group_name=group_name)
                    subject_1 = data.subject_1
                    subject_2 = data.subject_2
                else:
                    data = await get_st_dats(message.from_user.id, session_maker, group_name=None)
                    subject_1 = user_data['subject_1']
                    subject_2 = user_data['subject_2']
                students_name = user_data['students_name']
                print(students_name)

                print(group_name)

                t_name = data.t_fullname
                t_subject = data.teacher_subject
                sch_name = data.school_name

                district = data.district
                region = data.region


                try:
                    for st_id, st_name in zip(students_id, students_name):
                        await create_user(st_id, message.from_user.id, st_name, t_name, t_subject, sch_name, subject_1,
                                          subject_2, district, region, group_name, session_maker)
                except (ValueError):
                    await create_user(students_id[0], message.from_user.id, students_name[0], t_name, t_subject,
                                      sch_name,
                                      subject_1, subject_2, district, region, group_name, session_maker)
        except:
            pass


    await state.set_state(PostRegistration.edit_datas)

async def edit_add_students(call: types.CallbackQuery, state: FSMContext, session_maker:sessionmaker, bot:Bot):
    bool = await is_group_active(call.from_user.id, call.data[3:], session_maker)
    if bool:
        await bot.send_animation(call.from_user.id,
                                 'CgACAgIAAxkBAAIXKmShmmM8ixMcRjaqoKbVuPOI1_WPAAIXMAAC3b4QSW2R36HUv-pWLwQ',
                                 caption=f"O‘quvchini qo‘shish uchun uning ism-familiyasi yozilgan xabarini botga uzating (\"Переслать\" qiling)\n\nQo‘shib bo‘lganingizdan so'ng \"Qo‘shishni yakunlash\" tugmasini bosing",reply_markup=nend)
        cou = await count_students(call.from_user.id, call.data[3:], session_maker)
        await state.update_data(students_id=[], students_name=[], group_name=call.data[3:], cou=cou)
        await state.set_state(PostRegistration.add_students)
    else:

        await call.message.edit_text(
            f'{call.data[3:]} ushbu guruh Premium tarifi muddati tugagani uchun inaktiv holatga o‘tkazilgan.\n\n'
            f' Guruhni aktiv holatga o‘tkazib undan foydalanish  uchun yana Premium tarifini faollashtirishingiz kerak. '
            ' <b>Unutmang, Premiumni aktivlashtirib siz eng asosiysi loyihani davom etishi va siz uchun yangidan-yangi imkoniyatlar yaratishimiz uchun katta yordam bergan bo‘lasiz. Bizni qo‘llab-quvvatlayotganingiz uchun rahmat❤️</b>\n\n'
            '<i>Quyida kerakli tarifni tanlab, Click to‘lov tizimi orqali to‘lovni amalga oshirishingiz mumkin👇</i>',
            parse_mode="HTML"
            )

        await call.message.answer_invoice(title='30 kunlik Premiumni sotib olish',
                                          description='Premiumni rasmiylashtirish uchun karta ma\'lumotlaringizni kiriting ',
                                          payload='premium30',
                                          provider_token='398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065',
                                          currency='UZS',
                                          prices=[
                                              types.LabeledPrice(
                                                  label="Premium tarifi",
                                                  amount=2000000
                                              )
                                          ],
                                          need_name=True)

        await call.message.answer(
            f'Agar boshqa guruh tanlamoqchi bo‘lsangiz "Qaytadan tanlash🔁" tugmasini bosib o‘zgartirishingiz mumkin',
            reply_markup=re_choose_gr
        )


    


async def get_stats(call: types.CallbackQuery,state: FSMContext, session_maker: sessionmaker):
    user_data = await state.get_data()
    groupn = user_data['groupn']
    test_type = call.data[-2:]
    res=await get_st_scores(call.from_user.id,groupn, test_type, session_maker)
    # res = np.average(res)

    await call.message.edit_text(res, parse_mode="HTML")
    await state.set_state(PostRegistration.menu)
    await call.message.answer(f'Kerakli bo‘limni tanlang')
    
async def register_back(message: types.Message, state: FSMContext, bot: Bot, session_maker: sessionmaker):
    state_name = await state.get_state()
    if state_name == 'Registration:register_school_name':
        await register_t_name(message, state)
    elif state_name == 'Registration:register_t_name':
        await select_role(message, state)
    elif state_name == 'Registration:show_res':
        await select_role(message, state)
    elif state_name == 'Registration:register_subject':
        await register_school_name(message, state,bot)
    elif state_name == "Registration:register_students":
        await detect_subject(message, state, bot)
    elif state_name == 'PostRegistration:register_students_new':
        await new_detect_subject(message, state, bot, session_maker)
    elif state_name == 'PostRegistration:new_gr':
        await edit_datas(message, state, session_maker)

    elif state_name == "Registration:end":
        await register_students(message, state, session_maker)
    elif state_name == "StudentMenu:get_code":
        await check_online_test(message, state, session_maker)
    elif state_name == "StudentMenu:select_m_check_online":
        await student_menu(message, state,bot)


async def testsch(message: types.Message, arqredis: ArqRedis):
    await arqredis.enqueue_job('send_message', _defer_by=timedelta(seconds=10), chat_id=message.from_user.id, text='Tes')