import asyncio

from aiogram import types
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from arq import ArqRedis
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


from db.user import  wr_starter_db,is_group_active,premium_checker,get_expired_users,expire_date,create_user, get_st_ids, get_st_datas, add_answers, get_group_names, add_score, get_st_scores, \
     get_st_dats, get_ans_message, get_sub_names, get_t_sub, count_students, delete_student_r
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


async def select_role(message: types.Message, state: FSMContext):
    await message.answer("Kim sifatida davom ettirmoqchisiz", reply_markup=slct_role)
    await state.set_state(Registration.slkt_role)

async def student_menu(messag: types.Message|types.CallbackQuery, state: FSMContext,bot: Bot, id: int = None):
    print("sdsdsdsdsds")
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
            builder.add(types.InlineKeyboardButton(text=i, callback_data=f'sub_{i}'))
        builder.adjust(1)
        await message.answer("Qaysi ustoz olgan test natijasini ko‘rishni istaysiz?:",reply_markup=builder.as_markup())
    else:
        await message.answer('Siz hech qaysi guruhga qo‘shilmagansiz. Guruhga qo‘shilish uchun ustozingizga xabar bering')
        await student_menu(message, state, bot)
async def result_msg(call: types.CallbackQuery, state: FSMContext,bot:Bot, session_maker: sessionmaker):
    result = await get_ans_message(call.from_user.id,call.data[4:], session_maker)
    await call.message.answer(result.replace('%^', "\n"), parse_mode="HTML")
    await student_menu(call, state, bot, call.from_user.id)
async def tutorial(message: types.Message, state: FSMContext, session_maker: sessionmaker):
    await wr_starter_db(message.from_user.id, session_maker, message.from_user.full_name, message.from_user.username)

    await message.answer(f"Assalomu alaykum, {message.from_user.full_name}, boshlashdan oldin iltimos qo‘llanma bilan yaxshilab tanishib chiqing", reply_markup=clear, parse_mode="HTML")
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
                                   'Premium tarif rasmiylashtirganingizdan so‘ng siz imkoniyatlaringizni ikki barobar ko‘paytirasiz, ya\'ni 4 tagacha guruh, har bir guruhga 30 tagacha odam qo‘shish imkoniyatiga ega bo‘lasiz '
                                   'va <b>eng asosiysi loyihani davom etishi va siz uchun yangidan-yangi imkoniyatlar yaratishimiz uchun katta yordam berasiz</b>\n\n'
                                   '<i>Quyida Click to‘lov tizimi orqali to‘lovni amalga oshirishingiz mumkin</i>' , parse_mode="HTML"
                                  )
        await bot.send_invoice(
            chat_id=uid,
            title='Premiumni sotib olish',
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
    if call.data == "first_subject":
        await state.update_data(subject_1=subject_name)
        daraja = '📗Kiritgan guruhingiz uchun ikkinchi'
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
            title='Premiumni sotib olish',
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

        expire_dat=await expire_date(message.from_user.id, session_maker)

        msg=await message.answer(f'Muvaffaqiyatli to‘lov qilindi! Endi 30 kun davomida 30 tagacha o‘quvchidan iborat 4 tagacha guruh bilan ishlashingiz mumkin. Bizni qo‘llab-quvvatlaganingiz uchun rahmat❤️\n\nAgar guruh nomini kiritayotganingizda yoki o‘quvchi habarini jo‘natayotgan paytingiz to‘lovni amalga oshirgan b'
                             f'bo‘lsangiz, iltimos, guruh nomini qaytadan yozing yoki o‘quchi habarini qaytadan jo‘nating.\n\n'
                             f'Agar guruh tanlayotganingizda to‘lagan bo‘lsangiz, iltimos,  "Qaytadan tanlash🔁" tugmasini bosib shu guruhni qaytadan tanlang.\n\n\n'
                             f'<b>Premium obunani amal qilish muddati:</b> <code>{expire_dat}</code>', parse_mode="HTML")
        await bot.pin_chat_message(message.from_user.id, msg.message_id)



async def remove_from_premium(message: types.Message, session_maker: sessionmaker,bot: Bot):
    non_premiums = await get_expired_users(session_maker)
    if non_premiums != None:
        for np in non_premiums:

            msg=await bot.send_message(np, 'Afsuski, Premium tarifi muddatingiz yakunlandi. 2 ta guruhdagi 15 tadan tashqari barcha o‘quvchilar ma\'lumotlari inaktiv holatga o‘tadi va ulardan foydalana olmaysiz. '
                                       f'O‘quvchilar ma\'lumotlarini aktiv holatga o‘tkazib undan foydalanish uchun yana Premium tarifini faollashtirishingiz kerak. '
                ' <b>Unutmang, Premiumni aktivlashtirib siz eng asosiysi loyihani davom etishi va siz uchun yangidan-yangi imkoniyatlar yaratishimiz uchun katta yordam bergan bo‘lasiz. Bizni qo‘llab-quvvatlayotganingiz uchun rahmat❤️</b>\n\n'
                '<i>Quyida Click to‘lov tizimi orqali to‘lovni amalga oshirishingiz mumkin👇</i>',)






            await bot.send_invoice(np,title='Premiumni sotib olish',
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
                 datas.subject_1, datas.subject_2,test_type, session_maker, datas.teacher_subject)
    document = types.input_file.BufferedInputFile(file=save_to_title_pdf, filename='@ce_test_center_bot.pdf')
    await bot.send_document(message.chat.id, document=document)
    try:
        save_to_pdf, cvl,ivl = await create_pdf(save_to_io, test_type, datas.subject_1, datas.subject_2, datas.school_name, ids,
                                       d1, message.from_user.id, session_maker, datas.teacher_subject, book_type)
        document = types.input_file.BufferedInputFile(file=save_to_pdf, filename='@ce_test_center_bot.pdf')
        await bot.send_document(message.chat.id, document=document)
        if cvl != 'ove':
            await bot.send_message(message.chat.id,f'<b>Birinchi tarafi uchun:</b>\n\n<code>{cvl}</code>\n\n\n<b>Ikkinchi tarafi uchun: </b>\n\n<code>{ivl}</code>', parse_mode="HTML")

    except IndexError as e:
        await bot.send_message(message.chat.id,f"Jo'natilgan faylda testlar soni {test_type}tadan kam, yoki testlar xato kiritilgan")
        print('errort')


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
                                     '<i>Quyida Click to‘lov tizimi orqali to‘lovni amalga oshirishingiz mumkin👇</i>',
                                     parse_mode="HTML"
                                     )

        await call.message.answer_invoice(title='Premiumni sotib olish',
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
        await call.message.edit_text('Test kitobchasi shaklini tanlang:', reply_markup=k_select_book_type,  cache_time=1)
    else:
        await call.message.edit_text('Test kitobchasi shaklini tanlang:', reply_markup=k_select_book_type30,  cache_time=1)
async def send_file(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Testni namunada ko‘rsatilganidek shaklda jo‘nating va uyog‘ini bizga qo‘yib bering😊", reply_markup=back_2_menu,  cache_time=1)
    await state.set_state(PostRegistration.send_file)
    await state.update_data(bok_type=call.data[5:])

async def send_file30(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Testni namunada ko‘rsatilganidek shaklda jo‘nating va uyog‘ini bizga qo‘yib bering😊", reply_markup=back_2_menu,  cache_time=1)
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
            '<i>Quyida Click to‘lov tizimi orqali to‘lovni amalga oshirishingiz mumkin👇</i>',
            parse_mode="HTML"
            )

        await call.message.answer_invoice(title='Premiumni sotib olish',
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
        await new_detect_subject(message, state, bot)
    elif state_name == 'PostRegistration:new_gr':
        await edit_datas(message, state, session_maker)

    elif state_name == "Registration:end":
        await register_students(message, state, session_maker)


async def testsch(message: types.Message, arqredis: ArqRedis):
    await arqredis.enqueue_job('send_message', _defer_by=timedelta(seconds=10), chat_id=message.from_user.id, text='Tes')