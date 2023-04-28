import asyncio

from aiogram import types
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from sqlalchemy import select  # type: ignore
from sqlalchemy.orm import sessionmaker, joinedload, selectinload, Session  # type: ignore
from fsm import Registration, PostRegistration
# from bot.keyboards import clear, yes, back, end, keyboard, k_karakalpak, k_andijon, k_bukhara, k_jizzakh, k_qashqadaryo, k_A_NAVOIY, k_namangan, k_samarkand, k_surxondaryo, k_sirdaryo, k_tashkent_reg, k_fergana, k_xorazm, k_tashkent_city, k_regions,
from keyboards import *
from keyboards.reply import menu, back_2_menu, end_register, edit_menu, slct_role, student_key

from pdftool.string2pdf import create_title
from test_scanner.scanner import test_scanner_func
from io import BytesIO
from aiogram import html


from aiogram import Bot


from db.user import create_user, get_st_ids, get_st_datas, add_answers, get_group_names, add_score, get_st_scores, \
     get_st_dats, get_ans_message, get_sub_names, get_t_sub
from pdftool.utils import create_pdf

from db.user import get_stat
from keyboards.reply import test_type
from datetime import date
import time
import numpy as np

today = date.today()

# dd/mm/YY
d1 = today.strftime("%d.%m.%Y")

# async def send_mes(message: types.Message,bot: Bot):
#     await bot.send_message(1357099819,"Hello")

async def add_scor(message: types.Message, session_maker: sessionmaker):

    res=await get_st_scores(729659100, session_maker)
    # res = np.average(res)

    await message.answer(res, parse_mode="HTML")

async def select_role(message: types.Message, state: FSMContext):
    await message.answer("Kim sifatida davom ettirmoqchisiz", reply_markup=slct_role)
    await state.set_state(Registration.slkt_role)

async def student_menu(messag: types.Message|types.CallbackQuery, state: FSMContext,bot: Bot, id: int = None):
    print("sdsdsdsdsds")
    if not id:
        await messag.answer("Natijalarni ko‘rish", reply_markup=student_key)
    else:
        await bot.send_message(id,"Natijalarni ko‘rish", reply_markup=student_key)
    await state.set_state(Registration.show_res)
async def select_sub_name(message: types.Message,state: FSMContext,session_maker: sessionmaker):


    sub_names = await get_sub_names(int(message.from_user.id), session_maker)
    builder = InlineKeyboardBuilder()
    for i in sub_names:
        builder.add(types.InlineKeyboardButton(text=i, callback_data=f'sub_{i}'))
    builder.adjust(1)


    await message.answer("Qaysi ustoz olgan test natijasi:",reply_markup=builder.as_markup())
async def result_msg(call: types.CallbackQuery, state: FSMContext,bot:Bot, session_maker: sessionmaker):
    result = await get_ans_message(call.from_user.id,call.data[4:], session_maker)
    await call.message.answer(result.replace('%^', "\n"), parse_mode="HTML")
    await student_menu(call, state, bot, call.from_user.id)
async def tutorial(message: types.Message, state: FSMContext):
    await message.answer(f"Qo'llanmani o‘qib chiqing!🔤", reply_markup=clear, parse_mode="HTML")
    await state.set_state(Registration.tutorial)
    # await state.set_state(PostRegistration.menu)

async def register_t_name(message: types.Message, state: FSMContext):
    await message.answer(f"Ism familiyangiz rostan {message.from_user.full_name}mi?\n\nAgar ism to‘g‘ri bo‘lsa pastdagi 'Ha' tugmasini bosing, unday bo‘lmasa to‘g‘ri ismni jo‘nating", reply_markup=yes)
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







    await bot.send_message(useid,f"👤<b>ISM FAMILIYA:</b> {html.italic(html.quote(t_name))}\n\nAgar ism familiyangizda xatolik bo'lsa \"Ortga qaytish🔙\" tugmasini bosib qaytadan jo‘nating", parse_mode="HTML")
    await bot.send_message(useid,f"🏫O'quv muassasasi nomini jo‘nating:", reply_markup=back)
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

    await bot.send_message(useid,f'👤<b>ISM FAMILIYA:</b> {html.italic(html.quote(t_name))}\n🏫<b>O‘QUV MUASSASI NOMI:</b> {html.italic(html.quote(scname))}\n\n--------------------\n\n<i>Agar yuqoridagi ma’lumotlarda xatolik bo‘lsa \"Ortga qaytish🔙\" tugmasini bosib qaytadan jo‘natishingiz mumkin</i>\n\n', parse_mode="HTML")
    await bot.send_message(useid,'Kerakli hududni tanlang:',reply_markup=k_regions)
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


    await call.message.edit_text(f'👤<b>ISM FAMILIYA:</b> {html.italic(html.quote(t_name))}\n🏫<b>O‘QUV MUASSASI NOMI:</b> {html.italic(html.quote(scname))}\n<b>HUDUD:</b> <i>{call.data[7:]}</i>\n\n--------------------\n\n<i>Agar yuqoridagi ma’lumotlarda xatolik bo‘lsa \"Ortga qaytish🔙\" tugmasini bosib qaytadan jo‘natishingiz mumkin</i>\n\nO‘quv muassasi joylashgan tumanni tanlang:', reply_markup=key_var, parse_mode="HTML")




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







    await bot.send_message(useid,f"👤<b>ISM FAMILIYA:</b> {html.italic(html.quote(t_name))}\n🏫<b>O‘QUV MUASSASI NOMI:</b> {html.italic(html.quote(scname))}\n🏙<b>HUDUD:</b> <i>{region}</i>\n🏙<b>TUMAN:</b> {district}\n\n--------------------\n\n<i>Agar yuqoridagi ma’lumotlarda xatolik bo‘lsa \"Ortga qaytish🔙\" tugmasini bosib qaytadan jo‘natishingiz mumkin</i>\n\n", reply_markup=back, parse_mode="HTML")

    await bot.send_message(useid,f"Pastdan kerakli fanni tanlang:", reply_markup=keyboard)
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
                              f"🏫<b>O‘QUV MUASSASI NOMI:</b> {html.italic(html.quote(scname))}\n"
                              f"🏙<b>HUDUD:</b> <i>{region}</i>\n🏙<b>TUMAN:</b> {district}\n"
                              f"📚<b>FAN:</b> <i>{t_subject}</i>\n\n"
                              f"--------------------\n\n"
                              f"<i>Agar yuqoridagi ma’lumotlarda xatolik bo‘lsa \"Ortga qaytish🔙\" tugmasini bosib qaytadan jo‘natishingiz mumkin</i>\n\n", parse_mode="HTML")
    await call.message.answer(
        f"Guruh nomini kiriting:",
        reply_markup=back)
    await state.set_state(Registration.register_group_name)

async def register_new_group_name(message: types.Message, state: FSMContext, session_maker:sessionmaker):
    await message.answer('Yangi guruh nomi:', reply_markup=back)
    tsub = await get_t_sub(message.from_user.id, session_maker)
    await state.update_data(t_subject=tsub, user_id=message.from_user.id)
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

        await state.update_data(group_name= message.text)
        group_name = message.text
    except:
        group_name = user_data['group_name']
    await bot.send_message(useid,f"👤<b>ISM FAMILIYA:</b> {html.italic(html.quote(t_name))}\n"
                              f"🏫<b>O‘QUV MUASSASI NOMI:</b> {html.italic(html.quote(scname))}\n"
                              f"🏙<b>HUDUD:</b> <i>{region}</i>\n🏙<b>TUMAN:</b> {district}\n"
                              f"📚<b>FAN:</b> <i>{t_subject}</i>\n"
                                   f"👥<b>GURUH NOMI:</b> {html.italic(html.quote(group_name))}\n\n"
                              f"--------------------\n\n"
                              f"<i>Agar yuqoridagi ma’lumotlarda xatolik bo‘lsa \"Ortga qaytish🔙\" tugmasini bosib qaytadan jo‘natishingiz mumkin</i>\n\n", parse_mode="HTML")


    await bot.send_message(useid,
        f"{t_subject} nechanchi darajali fan:",
        reply_markup=k_select_subject_degree)

async def new_detect_subject(message: types.Message|types.CallbackQuery,state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    t_subject = user_data['t_subject']
    id = user_data['user_id']

    await bot.send_message(id,
        f"{t_subject} nechanchi darajali fan:",
        reply_markup=k_select_subject_degree)
    try:
        if message.text != "Ortga qaytish🔙":
            await state.update_data(group_name=message.text)
    except:
        pass

async def select_subject(call: types.CallbackQuery,state: FSMContext):
    user_data = await state.get_data()
    subject_name = user_data['t_subject']
    if call.data == "first_subject":
        await state.update_data(subject_1=subject_name)
        daraja = 'Ikkinchi'
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
        daraja = 'Birinchi'
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

    await  call.message.answer(f'{daraja} darajali fannni tanlang:', reply_markup=key_subject)



async def about_register_students(call: types.CallbackQuery,state: FSMContext):
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
                                  f"🏫<b>O‘QUV MUASSASI NOMI:</b> {html.italic(html.quote(scname))}\n"
                                  f"🏙<b>HUDUD:</b> <i>{region}</i>\n🏙<b>TUMAN:</b> {district}\n"
                                  f"📚<b>FAN:</b> <i>{t_subject}</i>\n"
                                  f"👥<b>GURUH NOMI:</b> {html.italic(html.quote(group_name))}\n"
                               f"👥<b>BIRINCHI DARAJALI FAN:</b> <i>{subject_1}</i>\n"
                               f"👥<b>IKKINCHI DARAJALI FAN:</b> <i>{subject_2}</i>\n\n"
                                  f"--------------------\n\n"
                                  f"<i>Agar yuqoridagi ma’lumotlarda xatolik bo‘lsa \"Ortga qaytish🔙\" tugmasini bosib qaytadan jo‘natishingiz mumkin</i>\n\n",
                           parse_mode="HTML")

    await call.message.answer(
        f"O'quvchini qo'shish uchun uning habarini botga uzating\n\nQo'shib bo'lganingizdan so'ng \"Qo'shishni yakunlash\" tugmasini bosing",
        reply_markup=end)
    print(call.data[:7])
    await state.update_data(subject=call.data[5:])
    await state.set_state(Registration.register_students)

async def new_about_register_st(call: types.CallbackQuery,state: FSMContext):
    if call.data.startswith('sub_s_first_'):
        print('2',call.data[12:])
        await state.update_data(subject_2=call.data[12:])

    else:
        print('1',call.data[13:])
        await state.update_data(subject_1=call.data[13:])

    await call.message.answer(
        f"O'quvchini qo'shish uchun uning habarini botga uzating\n\nQo'shib bo'lganingizdan so'ng \"Qo'shishni yakunlash\" tugmasini bosing",
        reply_markup=end)
    await state.update_data(students_id=[], students_name=[])
    await state.set_state(PostRegistration.register_students_new)


async def register_students(message: types.Message, state: FSMContext, session_maker: sessionmaker):

    user_data = await state.get_data()
    students_id=user_data['students_id']
    students_name =user_data['students_name']
    state_name = await state.get_state()

    if message.forward_from:
        await message.reply(f"O'quvchi ro'yxatga olindi")
        students_id.append(message.forward_from.id)
        students_name.append(message.text)

        print(message.forward_from)
    elif message.text == "Ortga qaytish🔙" and state_name =="Registration:end":
        await message.answer(
            f"O'quvchini qo'shish uchun uning habarini botga uzating\n\nQo'shib bo'lganingizdan so'ng \"Qo'shishni yakunlash\" tugmasini bosing",
            reply_markup=end)
        await state.set_state(Registration.register_students)
    elif message.text == "Ortga qaytish🔙" and state_name =="PostRegistration:add_students":
        await edit_datas(message, state, session_maker)

    elif message.text == "Ortga qaytish🔙" and state_name =="PostRegistration:register_students_new":
        await new_detect_subject(message, state, bot)

    elif not message.forward_from:
        await message.reply(f"O'quvchi tomonidan ma'lumotlari berkitilgan")










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
        await message.answer(f'Ro\'yxatdan o\'tishni yakunlandi', reply_markup=end_register)
        await state.set_state(Registration.end)
    else:
        await message.answer(f'O\'qvchi qo\'shilmagan, qaytadan qo\'shing', reply_markup=end)



#
async def reg_menu(message: types.Message, state: FSMContext):
    await message.answer(f'Kerakli bo\'limni tanlang', reply_markup=menu)
    await state.clear()
    await state.set_state(PostRegistration.menu)

async def get_file(message: types.Message, state: FSMContext, bot: Bot, session_maker: sessionmaker):
    user_data = await state.get_data()
    groupn = user_data['groupn']
    test_type = user_data['test_type']
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
                 datas.subject_1, datas.subject_2,test_type, session_maker, datas.teacher_subject)
    document = types.input_file.BufferedInputFile(file=save_to_title_pdf, filename='@ce_test_center_bot.pdf')
    await bot.send_document(message.chat.id, document=document)
    try:
        save_to_pdf = await create_pdf(save_to_io, test_type, datas.subject_1, datas.subject_2, datas.school_name, ids,
                                       d1, message.from_user.id, session_maker, datas.teacher_subject)
        document = types.input_file.BufferedInputFile(file=save_to_pdf, filename='@ce_test_center_bot.pdf')
        await bot.send_document(message.chat.id, document=document)
    except IndexError as e:
        await bot.send_message(message.chat.id,f"Jo'natilgan faylda testlar soni {test_type}tadan kam, yoki testlar xato kiritilgan")
        print('errort')


    # await state.update_data(checked_status=True)
    await reg_menu(message, state)

    # await message.answer_document(types.BufferedInputFile(file=save_to_io, filename='fdf.pdf'))

    # save_to_io.close()
    # save_to_pdf.close()
async def about_scan_test(message: types.Message, state: FSMContext):
    await message.answer('Natijalarni olish uchun titulni rasmga olib yuboring', reply_markup=back_2_menu)
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
        await message.reply("XATOLIK YUZ BERDI", parse_mode="HTML")
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

async def select_test_type(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(groupn=call.data[3:])
    await call.message.edit_text('Test shaklini tanlang:', reply_markup=test_type)


async def send_file(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    await call.message.answer("Fayl jo'nating", reply_markup=back_2_menu)
    await state.set_state(PostRegistration.send_file)
    await state.update_data(test_type=call.data[-2:])


async def callback_back(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    if call.data == 'district_back':
        await register_region(types.Message,state=state)
    elif call.data == 'select_back':
        await new_detect_subject(call, state, bot)


async def edit_datas(message: types.Message, state: FSMContext,session_maker: sessionmaker):
    state_name = await state.get_state()



    await message.answer('O\'zgartirish uchun ma\'lumotni tanlang', reply_markup=edit_menu)
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

async def edit_add_students(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(f"O'quvchini qo'shish uchun uning habarini botga uzating\n\nQo'shib bo'lganingizdan so'ng \"Qo'shishni yakunlash\" tugmasini bosing",
        reply_markup=end)
    await state.update_data(students_id=[], students_name=[], group_name=call.data[3:])
    await state.set_state(PostRegistration.add_students)


async def get_stats(call: types.CallbackQuery,state: FSMContext, session_maker: sessionmaker):
    user_data = await state.get_data()
    groupn = user_data['groupn']
    test_type = call.data[-2:]
    res=await get_st_scores(call.from_user.id,groupn, test_type, session_maker)
    # res = np.average(res)

    await call.message.edit_text(res, parse_mode="HTML")
    await call.message.answer(f'Kerakli bo\'limni tanlang')
    await state.set_state(PostRegistration.menu)
async def register_back(message: types.Message, state: FSMContext, bot: Bot, session_maker: sessionmaker):
    state_name = await state.get_state()
    if state_name == 'Registration:register_school_name':
        await register_t_name(message, state)
    elif state_name == 'Registration:register_t_name':
        await select_role(message, state)
    elif state_name == 'Registration:show_res':
        await select_role(message, state)
    elif state_name == 'Registration:register_subject':
        await register_school_name(message, state)
    elif state_name == "Registration:register_students":
        await register_subject(message, state, bot)
    elif state_name == 'PostRegistration:register_students_new':
        await new_detect_subject(message, state, bot)

    elif state_name == "Registration:end":
        await register_students(message, state, session_maker)

