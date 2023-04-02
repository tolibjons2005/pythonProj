from aiogram import types
from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from sqlalchemy import select  # type: ignore
from sqlalchemy.orm import sessionmaker, joinedload, selectinload  # type: ignore
from bot.fsm import Registration, PostRegistration
# from bot.keyboards import clear, yes, back, end, keyboard, k_karakalpak, k_andijon, k_bukhara, k_jizzakh, k_qashqadaryo, k_A_NAVOIY, k_namangan, k_samarkand, k_surxondaryo, k_sirdaryo, k_tashkent_reg, k_fergana, k_xorazm, k_tashkent_city, k_regions,
from bot.keyboards import *
from bot.keyboards.reply import menu, back_2_menu, end_register

from bot.pdftool.string2pdf import create_title
from bot.test_scanner.scanner import test_scanner_func
from io import BytesIO


from aiogram import Bot


from bot.db.user import create_user, get_st_ids, get_st_datas, add_answers
from bot.pdftool.utils import create_pdf


async def tutorial(message: types.Message, state: FSMContext):
    await message.answer("Qo'llanmani o‘qib chiqing!", reply_markup=clear)
    await state.set_state(Registration.tutorial)

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







    await bot.send_message(useid,f"ISM FAMILIYA: {t_name}\n\nAgar ism familiyangizda xatolik bo'lsa \"Ortga qaytish\" tugmasini bosib qaytadan jo‘nating")
    await bot.send_message(useid,f"O'quv muassasasi nomini jo‘nating:", reply_markup=back)
    await state.set_state(Registration.register_school_name)


async def register_region(message: types.Message, state: FSMContext,  bot: Bot):
    try:
        scname = message.text
        await state.update_data(sc_name=scname)
    except:
        pass
    user_data = await state.get_data()
    useid = user_data['t_id']
    await bot.send_message(useid,'Hududni tanalang:',reply_markup=k_regions)

async def register_district(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(region=call.data[7:])
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


    await call.message.edit_text('Hududni tanalang:', reply_markup=key_var)




async def register_subject(call: types.CallbackQuery, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    scname = user_data['sc_name']
    useid = user_data['t_id']




    await state.update_data(students_id=[], students_name=[])
    try:
        await state.update_data(district=call.data[9:])
    except:
        pass







    await bot.send_message(useid,f"ISM FAMILIYA: {user_data['t_name']}\n\n"
                         f"O'QUV MUASSASI NOMI: {scname}\n\n"
                         f"--------------------\n\nAgar ism familiyangizda xatolik bo'lsa \"Ortga qaytish\" tugmasini bosib qaytadan jo‘nating", reply_markup=back)

    await bot.send_message(useid,f"Pastdan kerakli fanni tanlang:", reply_markup=keyboard)
    await state.set_state(Registration.register_subject)

async def register_group_name(call: types.CallbackQuery,state: FSMContext):
    if call.data == 'detect_back':
        pass
    else:
        await state.update_data(t_subject=call.data[5:])
    await call.message.answer(
        f"Guruh nomini kiriting:",
        reply_markup=back)
    await state.set_state(Registration.register_group_name)

async def detect_subject(message: types.Message,state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    subject_name = user_data['t_subject']
    useid = user_data['t_id']
    try:

        await state.update_data(group_name= message.text)
    except:
        pass


    await bot.send_message(useid,
        f"{subject_name.replace('_',' ')} nechanchi darajali fan:",
        reply_markup=k_select_subject_degree)
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
        elif subject_name == 'Ingliz_tili':
            key_subject = k_first_english
        elif subject_name == 'Fransuz_tili':
            key_subject = k_first_french
        elif subject_name == 'Tarix':
            key_subject = k_first_history
        elif subject_name == 'Nemis_tili':
            key_subject = k_first_deutsch
        elif subject_name == 'Rus_tili_va_adabiyoti':
            key_subject = k_first_russian
        elif subject_name == 'Ona_tili_va_adabiyoti':
            key_subject = k_first_mother_t
        elif subject_name == 'Geografiya':
            key_subject = k_first_geography
        elif subject_name == 'Matematika':
            key_subject = k_first_math
        elif subject_name == 'Qoraqalpoq_tili_va_adabiyoti':
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
        elif subject_name == 'Ingliz_tili':
            key_subject = k_second_english
        elif subject_name == 'Fransuz_tili':
            key_subject = k_second_french
        elif subject_name == 'Tarix':
            key_subject = k_second_history
        elif subject_name == 'Nemis_tili':
            key_subject = k_second_deutsch
        elif subject_name == 'Rus_tili_va_adabiyoti':
            key_subject = k_second_russian
        elif subject_name == 'Ona_tili_va_adabiyoti':
            key_subject = k_second_mother_t
        elif subject_name == 'Geografiya':
            key_subject = k_second_geography
        elif subject_name == 'Matematika':
            key_subject = k_second_math
        elif subject_name == 'Qoraqalpoq_tili_va_adabiyoti':
            key_subject = k_second_karakalpak

    await  call.message.answer(f'{daraja} darajali fannni tanlang:', reply_markup=key_subject)

async def about_register_students(call: types.CallbackQuery,state: FSMContext):
    if call.data.startswith('sub_s_first_'):
        print('2',call.data[12:])
        await state.update_data(subject_2=call.data[12:])
    else:
        print('1',call.data[13:])
        await state.update_data(subject_1=call.data[13:])
    await call.message.answer(
        f"O'quvchini qo'shish uchun uning habarini botga uzating\n\nQo'shib bo'lganingizdan so'ng \"Qo'shishni yakunlash\" tugmasini bosing",
        reply_markup=end)
    print(call.data[:7])
    await state.update_data(subject=call.data[5:])
    await state.set_state(Registration.register_students)
async def register_students(message: types.Message, state: FSMContext ):

    user_data = await state.get_data()
    students_id=user_data['students_id']
    students_name =user_data['students_name']

    if message.forward_from:
        await message.reply(f"O'quvchi ro'yxatga olindi")
        students_id.append(message.forward_from.id)
        students_name.append(message.text)

        print(message.forward_from)
    elif message.text == "Ortga qaytish":
        await message.answer(
            f"O'quvchini qo'shish uchun uning habarini botga uzating\n\nQo'shib bo'lganingizdan so'ng \"Qo'shishni yakunlash\" tugmasini bosing",
            reply_markup=end)
        await state.set_state(Registration.register_students)
    elif not message.forward_from:
        await message.reply(f"O'quvchi tomonidan ma'lumotlari berkitilgan")











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
    try:
        for st_id, st_name in zip(students_id, students_name):
            await create_user(st_id, message.from_user.id, st_name, t_name, t_subject,sch_name,subject_1, subject_2, district, region,group_name, session_maker)
    except (ValueError):
        await create_user(students_id[0], message.from_user.id, students_name[0], t_name, t_subject, sch_name,subject_1, subject_2, district, region, group_name,session_maker)

    await message.answer(f'Ro\'yxatdan o\'tishni yakunlandi', reply_markup=end_register)
    await state.set_state(Registration.end)

#
async def reg_menu(message: types.Message, state: FSMContext):
    await message.answer(f'Fayl jo\'nat', reply_markup=menu)
    await state.clear()
    await state.set_state(PostRegistration.menu)

async def get_file(message: types.Message, state: FSMContext, bot: Bot, session_maker: sessionmaker):
    save_to_io = BytesIO()
    save_to_pdf = BytesIO()
    save_to_title_pdf = BytesIO()
    await bot.download(
        message.document,
        destination=save_to_io
    )
    ids = await get_st_ids(int(message.from_user.id), session_maker)
    datas = await get_st_datas(int(message.from_user.id), session_maker)
    save_to_title_pdf=create_title(ids, message.from_user.id, datas.school_name, '20.03.2023', datas.group_name,
                 datas.subject_1, datas.subject_2)
    document = types.input_file.BufferedInputFile(file=save_to_title_pdf, filename='document.pdf')
    await bot.send_document(message.chat.id, document=document)
    save_to_pdf=await create_pdf(save_to_io, '90',  datas.subject_1, datas.subject_2,datas.school_name,ids,'12.03.2023',message.from_user.id, session_maker)
    document = types.input_file.BufferedInputFile(file=save_to_pdf, filename='document.pdf')
    await bot.send_document(message.chat.id, document=document)
    # await state.update_data(checked_status=True)
    await reg_menu(message, state)

    # await message.answer_document(types.BufferedInputFile(file=save_to_io, filename='fdf.pdf'))

    # save_to_io.close()
    # save_to_pdf.close()
async def about_scan_test(message: types.Message, state: FSMContext):
    await message.answer('Natijalarni olish uchun titulni rasmga olib yuboring', reply_markup=back_2_menu)
    await state.set_state(PostRegistration.scan_test)

async def scan_test(message: types.Message, state: FSMContext, bot: Bot,session_maker: sessionmaker):
    photo_io = BytesIO()
    await bot.download(
        message.photo[-1],
        destination=photo_io
    )
    grading, resultg = await test_scanner_func(photo_io,session_maker)
    await message.answer(str(resultg))


async def send_file(message: types.Message, state: FSMContext, bot: Bot):
    await message.answer("Fayl jo'nating", reply_markup=back_2_menu)
    await state.set_state(PostRegistration.send_file)


async def callback_back(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'district_back':
        await register_region(types.Message,state=state)

async def register_back(message: types.Message, state: FSMContext, bot: Bot):
    state_name = await state.get_state()
    if state_name == 'Registration:register_school_name':
        await register_t_name(message, state)
    elif state_name == 'Registration:register_subject':
        await register_school_name(message, state)
    elif state_name == "Registration:register_students":
        await register_subject(message, state, bot)

    elif state_name == "Registration:end":
        await register_students(message, state)

