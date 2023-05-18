from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
# menu =ReplyKeyboardMarkup([
#     [KeyboardButton(text='Press')]
# ], resize_keyboard=True )

# clear =ReplyKeyboardMarkup([[KeyboardButton(text="O‘rganib chiqdim")]], resize_keyboard=True )

clear = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='O‘rganib chiqdim'), ],
    ],
    resize_keyboard=True
)
#
yes =ReplyKeyboardMarkup(
    keyboard=[
    [KeyboardButton(text="Ha")]
], resize_keyboard=True, input_field_placeholder='Tolibjon Komiljonov' )

async def back(txt):
    bac = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Ortga qaytish🔙")]
        ], resize_keyboard=True, input_field_placeholder=txt, one_time_keyboard=True)
    return bac

#
back_2_menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Asosiy menyuga qaytish🔙")]
], resize_keyboard=True )
end_register = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text="Ro‘yxatdan o‘tishni yakunlash")],
[KeyboardButton(text="Ortga qaytish🔙")]
], resize_keyboard=True )
menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Test yaratish📝"),KeyboardButton(text="Natijalarni tekshirish✅❌")], [KeyboardButton(text="Ma'lumotlarni tahrirlash✏️")], [KeyboardButton(text="Statistika📊")]], resize_keyboard=True)
end = ReplyKeyboardMarkup(
    keyboard=[
    [KeyboardButton(text="Qo'shishni yakunlash")],

    [KeyboardButton(text="Ortga qaytish🔙")]
], resize_keyboard=True )

edit_menu = ReplyKeyboardMarkup(
    keyboard=[
    [KeyboardButton(text="O'quvchi qo'shish")],

[KeyboardButton(text="Yangi guruh qo'shish")],


    [KeyboardButton(text="Asosiy menyuga qaytish🔙")],

], resize_keyboard=True )
slct_role = ReplyKeyboardMarkup(
    keyboard=[
    [KeyboardButton(text="O‘qituvchi")],


    [KeyboardButton(text="O‘quvchi")],
[KeyboardButton(text="Ortga qaytish🔙")]
], resize_keyboard=True )
student_key = ReplyKeyboardMarkup(
    keyboard=[
    [KeyboardButton(text="Ohirgi natijani ko‘rish")],



[KeyboardButton(text="Ortga qaytish🔙")]
], resize_keyboard=True )
test_type = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='90 talik (blok)', callback_data="test_type_90")],[InlineKeyboardButton(text='30 talik', callback_data="test_type_30")]])


buttons = [
    [InlineKeyboardButton(text="Biologiya", callback_data="data_Biologiya"),
    InlineKeyboardButton(text="Fizika", callback_data="data_Fizika")],
    [InlineKeyboardButton(text="Kimyo", callback_data="data_Kimyo"),
    InlineKeyboardButton(text="Ingliz tili", callback_data="data_Ingliz_tili")],
    [InlineKeyboardButton(text="Fransuz tili", callback_data="data_Fransuz_tili"),
    InlineKeyboardButton(text="Tarix", callback_data="data_Tarix")],
    [InlineKeyboardButton(text="Nemis tili", callback_data="data_Nemis_tili"),
    InlineKeyboardButton(text="Rus tili va adabiyoti", callback_data="data_Rus_tili_va_adabiyoti")],
    [InlineKeyboardButton(text="Ona tili va adabiyoti", callback_data="data_Ona_tili_va_adabiyoti"),
    InlineKeyboardButton(text="Geografiya", callback_data="data_Geografiya")],
    [InlineKeyboardButton(text="Qoraqalpoq tili va adabiyoti", callback_data="data_Qoraqalpoq_tili_va_adabiyoti"),
    InlineKeyboardButton(text="Matematika", callback_data="data_Matematika")],
    [InlineKeyboardButton(text="Ortga qaytish🔙", callback_data="subject_back")]

    ]

keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
karakalpak = [
[InlineKeyboardButton(text="Nukus shahri", callback_data="district_Nukus shahri"),
InlineKeyboardButton(text="Amudaryo tumani", callback_data="district_Amudaryo tumani")],
[InlineKeyboardButton(text="Beruniy tumani", callback_data="district_Beruniy tumani"),
InlineKeyboardButton(text="Kegeyli tumani", callback_data="district_Kegeyli tumani")],
[InlineKeyboardButton(text="Qanliko‘l tumani", callback_data="district_Qanliko‘l tumani"),
InlineKeyboardButton(text="Qorao‘zak tumani", callback_data="district_Qorao‘zak tumani")],
[InlineKeyboardButton(text="Qo‘ng‘irot tumani", callback_data="district_Qo‘ng‘irot tumani"),
InlineKeyboardButton(text="Mo‘ynoq tumani", callback_data="district_Mo‘ynoq tumani")],
[InlineKeyboardButton(text="Nukus tumani", callback_data="district_Nukus tumani"),
InlineKeyboardButton(text="Taxiatosh tumani", callback_data="district_Taxiatosh tumani")],
[InlineKeyboardButton(text="Taxtako‘pir tumani", callback_data="district_Taxtako‘pir tumani"),
InlineKeyboardButton(text="To‘rtko‘l tumani", callback_data="district_To‘rtko‘l tumani")],
[InlineKeyboardButton(text="Xo‘jayli tumani", callback_data="district_Xo‘jayli tumani"),
InlineKeyboardButton(text="Chimboy tumani", callback_data="district_Chimboy tumani")],
[InlineKeyboardButton(text="Sho‘manoy tumani", callback_data="district_Sho‘manoy tumani"),
InlineKeyboardButton(text="Ellikqal’a tuman", callback_data="district_Ellikqal’a tuman")],
[InlineKeyboardButton(text="Ortga qaytish🔙", callback_data="district_back")]
]

k_karakalpak = InlineKeyboardMarkup(inline_keyboard=karakalpak)


andijon= [
[InlineKeyboardButton(text="Andijon shahri", callback_data="district_Andijon shahri"),
InlineKeyboardButton(text="Xonabod shahri", callback_data="district_Xonabod shahri")],
[InlineKeyboardButton(text="Andijon tumani", callback_data="district_Andijon tumani"),
InlineKeyboardButton(text="Asaka tumani", callback_data="district_Asaka tumani")],
[InlineKeyboardButton(text="Baliqchi tumani", callback_data="district_Baliqchi tumani"),
InlineKeyboardButton(text="Bo‘z tumani", callback_data="district_Bo‘z tumani")],
[InlineKeyboardButton(text="Buloqboshi tumani", callback_data="district_Buloqboshi tumani"),
InlineKeyboardButton(text="Jalaquduq tumani", callback_data="district_Jalaquduq tumani")],
[InlineKeyboardButton(text="Izboskan tumani", callback_data="district_Izboskan tumani"),
InlineKeyboardButton(text="Qo‘rg‘ontepa tumani", callback_data="district_Qo‘rg‘ontepa tumani")],
[InlineKeyboardButton(text="Marhamat tumani.", callback_data="district_Marhamat tumani."),
InlineKeyboardButton(text="Oltinko‘l tumani", callback_data="district_Oltinko‘l tumani")],
[InlineKeyboardButton(text="Paxtaobod tumani", callback_data="district_Paxtaobod tumani"),
InlineKeyboardButton(text="Ulug‘nor tumani", callback_data="district_Ulug‘nor tumani")],
[InlineKeyboardButton(text="Xo‘jaobod tumani", callback_data="district_Xo‘jaobod tumani"),
InlineKeyboardButton(text="Shahrixon tuman", callback_data="district_Shahrixon tuman")],
[InlineKeyboardButton(text="Ortga qaytish🔙", callback_data="district_back")]
]

k_andijon=InlineKeyboardMarkup(inline_keyboard=andijon)

bukhara= [
[InlineKeyboardButton(text="Buxoro shahri", callback_data="district_Buxoro shahri"),
InlineKeyboardButton(text="Kogon shahri", callback_data="district_Kogon shahri")],
[InlineKeyboardButton(text="Buxoro tumani", callback_data="district_Buxoro tumani"),
InlineKeyboardButton(text="Vobkent tumani", callback_data="district_Vobkent tumani")],
[InlineKeyboardButton(text="Jondor tumani", callback_data="district_Jondor tumani"),
InlineKeyboardButton(text="Kogon tumani", callback_data="district_Kogon tumani")],
[InlineKeyboardButton(text="Olot tumani", callback_data="district_Olot tumani"),
InlineKeyboardButton(text="Peshku tumani", callback_data="district_Peshku tumani")],
[InlineKeyboardButton(text="Romitan tumani", callback_data="district_Romitan tumani"),
InlineKeyboardButton(text="Shofirkon tumani", callback_data="district_Shofirkon tumani")],
[InlineKeyboardButton(text="Qorovulbozor tumani", callback_data="district_Qorovulbozor tumani"),
InlineKeyboardButton(text="Qorako‘l tumani", callback_data="district_Qorako‘l tumani")],
[InlineKeyboardButton(text="G‘ijduvon tuman", callback_data="district_G‘ijduvon tuman")],
[InlineKeyboardButton(text="Ortga qaytish🔙", callback_data="district_back")]
]

k_bukhara = InlineKeyboardMarkup(inline_keyboard=bukhara)

jizzakh = [
[InlineKeyboardButton(text="Jizzax shahri", callback_data="district_Jizzax shahri"),
InlineKeyboardButton(text="Arnasoy tumani", callback_data="district_Arnasoy tumani")],
[InlineKeyboardButton(text="Baxmal tumani", callback_data="district_Baxmal tumani"),
InlineKeyboardButton(text="Do‘stlik tumani", callback_data="district_Do‘stlik tumani")],
[InlineKeyboardButton(text="Zarbdor tumani", callback_data="district_Zarbdor tumani"),
InlineKeyboardButton(text="Zafarobod tumani", callback_data="district_Zafarobod tumani")],
[InlineKeyboardButton(text="Zomin tumani", callback_data="district_Zomin tumani"),
InlineKeyboardButton(text="Mirzacho‘l tumani", callback_data="district_Mirzacho‘l tumani")],
[InlineKeyboardButton(text="Paxtakor tumani", callback_data="district_Paxtakor tumani"),
InlineKeyboardButton(text="Forish tumani", callback_data="district_Forish tumani")],
[InlineKeyboardButton(text="Sharof Rashidov tumani", callback_data="district_Sharof Rashidov tumani"),
InlineKeyboardButton(text="G‘allaorol tumani", callback_data="district_G‘allaorol tumani")],
[InlineKeyboardButton(text="Yangiobod tuman", callback_data="district_Yangiobod tuman")],
[InlineKeyboardButton(text="Ortga qaytish🔙", callback_data="district_back")]
]

k_jizzakh = InlineKeyboardMarkup(inline_keyboard=jizzakh)

qashqadaryo = [
[InlineKeyboardButton(text="Qarshi shahri", callback_data="district_Qarshi shahri"),
InlineKeyboardButton(text="Shahrisabz shahri", callback_data="district_Shahrisabz shahri")],
[InlineKeyboardButton(text="Dehqonobod tumani", callback_data="district_Dehqonobod tumani"),
InlineKeyboardButton(text="Kasbi tumani", callback_data="district_Kasbi tumani")],
[InlineKeyboardButton(text="Kitob tumani", callback_data="district_Kitob tumani"),
InlineKeyboardButton(text="Koson tumani", callback_data="district_Koson tumani")],
[InlineKeyboardButton(text="Mirishkor tumani", callback_data="district_Mirishkor tumani"),
InlineKeyboardButton(text="Muborak tumani", callback_data="district_Muborak tumani")],
[InlineKeyboardButton(text="Nishon tumani", callback_data="district_Nishon tumani"),
InlineKeyboardButton(text="Chiroqchi tumani", callback_data="district_Chiroqchi tumani")],
[InlineKeyboardButton(text="Shahrisabz tumani", callback_data="district_Shahrisabz tumani"),
InlineKeyboardButton(text="Yakkabog‘ tumani", callback_data="district_Yakkabog‘ tumani")],
[InlineKeyboardButton(text="Qamashi tumani", callback_data="district_Qamashi tumani"),
InlineKeyboardButton(text="Qarshi tumani", callback_data="district_Qarshi tumani")],
[InlineKeyboardButton(text="G‘uzor tuman", callback_data="district_G‘uzor tuman")],
[InlineKeyboardButton(text="Ortga qaytish🔙", callback_data="district_back")]
]

k_qashqadaryo = InlineKeyboardMarkup(inline_keyboard=qashqadaryo)

A_NAVOIY = [
[InlineKeyboardButton(text="Navoiy shahri", callback_data="district_Navoiy shahri"),
InlineKeyboardButton(text="Zarafshon shahri", callback_data="district_Zarafshon shahri")],
[InlineKeyboardButton(text="Karmana tumani", callback_data="district_Karmana tumani"),
InlineKeyboardButton(text="Konimex tumani", callback_data="district_Konimex tumani")],
[InlineKeyboardButton(text="Navbahor tumani", callback_data="district_Navbahor tumani"),
InlineKeyboardButton(text="Nurota tumani", callback_data="district_Nurota tumani")],
[InlineKeyboardButton(text="Tomdi tumani", callback_data="district_Tomdi tumani"),
InlineKeyboardButton(text="Uchquduq tumani", callback_data="district_Uchquduq tumani")],
[InlineKeyboardButton(text="Xatirchi tumani", callback_data="district_Xatirchi tumani"),
InlineKeyboardButton(text="Qiziltepa tuman", callback_data="district_Qiziltepa tuman")],
[InlineKeyboardButton(text="Ortga qaytish🔙", callback_data="district_back")]
]

k_A_NAVOIY= InlineKeyboardMarkup(inline_keyboard=A_NAVOIY)

namangan = [
[InlineKeyboardButton(text="Namangan shahri", callback_data="district_Namangan shahri"),
InlineKeyboardButton(text="Kosonsoy tumani", callback_data="district_Kosonsoy tumani")],
[InlineKeyboardButton(text="Mingbuloq tumani", callback_data="district_Mingbuloq tumani"),
InlineKeyboardButton(text="Namangan tumani", callback_data="district_Namangan tumani")],
[InlineKeyboardButton(text="Norin tumani", callback_data="district_Norin tumani"),
InlineKeyboardButton(text="Pop tumani", callback_data="district_Pop tumani")],
[InlineKeyboardButton(text="To‘raqo‘rg‘on tumani", callback_data="district_To‘raqo‘rg‘on tumani"),
InlineKeyboardButton(text="Uychi tumani", callback_data="district_Uychi tumani")],
[InlineKeyboardButton(text="Uchqo‘rg‘on tumani", callback_data="district_Uchqo‘rg‘on tumani"),
InlineKeyboardButton(text="Chortoq tumani", callback_data="district_Chortoq tumani")],
[InlineKeyboardButton(text="Chust tumani", callback_data="district_Chust tumani"),
InlineKeyboardButton(text="Yangiqo‘rg‘on tuman", callback_data="district_Yangiqo‘rg‘on tuman")],
[InlineKeyboardButton(text="Ortga qaytish🔙", callback_data="district_back")]
]

k_namangan = InlineKeyboardMarkup(inline_keyboard=namangan)


samarkand = [
[InlineKeyboardButton(text="Samarqand shahri", callback_data="district_Samarqand shahri"),
InlineKeyboardButton(text="Kattaqo‘rg‘on shahri", callback_data="district_Kattaqo‘rg‘on shahri")],
[InlineKeyboardButton(text="Bulung‘ur tumani", callback_data="district_Bulung‘ur tumani"),
InlineKeyboardButton(text="Jomboy tumani", callback_data="district_Jomboy tumani")],
[InlineKeyboardButton(text="Ishtixon tumani", callback_data="district_Ishtixon tumani"),
InlineKeyboardButton(text="Kattaqo‘rg‘on tumani", callback_data="district_Kattaqo‘rg‘on tumani")],
[InlineKeyboardButton(text="Narpay tumani", callback_data="district_Narpay tumani"),
InlineKeyboardButton(text="Nurobod tumani", callback_data="district_Nurobod tumani")],
[InlineKeyboardButton(text="Oqdaryo tumani", callback_data="district_Oqdaryo tumani"),
InlineKeyboardButton(text="Payariq tumani", callback_data="district_Payariq tumani")],
[InlineKeyboardButton(text="Pastdarg‘om tumani", callback_data="district_Pastdarg‘om tumani"),
InlineKeyboardButton(text="Paxtachi tumani", callback_data="district_Paxtachi tumani")],
[InlineKeyboardButton(text="Samarqand tumani", callback_data="district_Samarqand tumani"),
InlineKeyboardButton(text="Toyloq tumani", callback_data="district_Toyloq tumani")],
[InlineKeyboardButton(text="Urgut tumani", callback_data="district_Urgut tumani"),
InlineKeyboardButton(text="Qo‘shrabot tuman", callback_data="district_Qo‘shrabot tuman")],
[InlineKeyboardButton(text="Ortga qaytish🔙", callback_data="district_back")]
]

k_samarkand = InlineKeyboardMarkup(inline_keyboard=namangan)


surxondaryo = [
[InlineKeyboardButton(text="Termiz shahri", callback_data="district_Termiz shahri"),
InlineKeyboardButton(text="Angor tumani", callback_data="district_Angor tumani")],
[InlineKeyboardButton(text="Boysun tumani", callback_data="district_Boysun tumani"),
InlineKeyboardButton(text="Denov tumani", callback_data="district_Denov tumani")],
[InlineKeyboardButton(text="Jarqo‘rg‘on tumani", callback_data="district_Jarqo‘rg‘on tumani"),
InlineKeyboardButton(text="Muzrobod tumani", callback_data="district_Muzrobod tumani")],
[InlineKeyboardButton(text="Oltinsoy tumani", callback_data="district_Oltinsoy tumani"),
InlineKeyboardButton(text="Sariosiyo tumani", callback_data="district_Sariosiyo tumani")],
[InlineKeyboardButton(text="Termiz tumani", callback_data="district_Termiz tumani"),
InlineKeyboardButton(text="Uzun tumani", callback_data="district_Uzun tumani")],
[InlineKeyboardButton(text="Sherobod tumani", callback_data="district_Sherobod tumani"),
InlineKeyboardButton(text="Sho‘rchi tumani", callback_data="district_Sho‘rchi tumani")],
[InlineKeyboardButton(text="Qiziriq tumani", callback_data="district_Qiziriq tumani"),
InlineKeyboardButton(text="Qumqo‘rg‘on tuman", callback_data="district_Qumqo‘rg‘on tuman")],
[InlineKeyboardButton(text="Ortga qaytish🔙", callback_data="district_back")]
]

k_surxondaryo = InlineKeyboardMarkup(inline_keyboard=surxondaryo)

sirdaryo =[
[InlineKeyboardButton(text="Guliston shahri", callback_data="district_Guliston shahri"),
InlineKeyboardButton(text="Yangiyer shahri", callback_data="district_Yangiyer shahri")],
[InlineKeyboardButton(text="Shirin shahri", callback_data="district_Shirin shahri"),
InlineKeyboardButton(text="Boyovut tumani", callback_data="district_Boyovut tumani")],
[InlineKeyboardButton(text="Guliston tumani", callback_data="district_Guliston tumani"),
InlineKeyboardButton(text="Mirzaobod tumani", callback_data="district_Mirzaobod tumani")],
[InlineKeyboardButton(text="Oqoltin tumani", callback_data="district_Oqoltin tumani"),
InlineKeyboardButton(text="Sardoba tumani", callback_data="district_Sardoba tumani")],
[InlineKeyboardButton(text="Sayxunobod tumani", callback_data="district_Sayxunobod tumani"),
InlineKeyboardButton(text="Sirdaryo tumani", callback_data="district_Sirdaryo tumani")],
[InlineKeyboardButton(text="Xovos tuman", callback_data="district_Xovos tuman")],
[InlineKeyboardButton(text="Ortga qaytish🔙", callback_data="district_back")]
]

k_sirdaryo = InlineKeyboardMarkup(inline_keyboard=surxondaryo)

tashkent_reg = [
[InlineKeyboardButton(text="Nurafshon shahri", callback_data="district_Nurafshon shahri"),
InlineKeyboardButton(text="Angren shahri", callback_data="district_Angren shahri")],
[InlineKeyboardButton(text="Bekobod shahri", callback_data="district_Bekobod shahri"),
InlineKeyboardButton(text="Olmaliq shahri", callback_data="district_Olmaliq shahri")],
[InlineKeyboardButton(text="Ohangaron shahri", callback_data="district_Ohangaron shahri"),
InlineKeyboardButton(text="Chirchiq shahri", callback_data="district_Chirchiq shahri")],
[InlineKeyboardButton(text="Yangiyo‘l shahri", callback_data="district_Yangiyo‘l shahri"),
InlineKeyboardButton(text="Bekobod tumani", callback_data="district_Bekobod tumani")],
[InlineKeyboardButton(text="Bo‘ka tumani", callback_data="district_Bo‘ka tumani"),
InlineKeyboardButton(text="Bo‘stonliq tumani", callback_data="district_Bo‘stonliq tumani")],
[InlineKeyboardButton(text="Zangiota tumani", callback_data="district_Zangiota tumani"),
InlineKeyboardButton(text="Qibray tumani", callback_data="district_Qibray tumani")],
[InlineKeyboardButton(text="Quyichirchiq tumani", callback_data="district_Quyichirchiq tumani"),
InlineKeyboardButton(text="Oqqo‘rg‘on tumani", callback_data="district_Oqqo‘rg‘on tumani")],
[InlineKeyboardButton(text="Ohangaron tumani", callback_data="district_Ohangaron tumani"),
InlineKeyboardButton(text="Parkent tumani", callback_data="district_Parkent tumani")],
[InlineKeyboardButton(text="Piskent tumani", callback_data="district_Piskent tumani"),
InlineKeyboardButton(text="Toshkent tumani", callback_data="district_Toshkent tumani")],
[InlineKeyboardButton(text="O‘rtachirchiq tumani", callback_data="district_O‘rtachirchiq tumani"),
InlineKeyboardButton(text="Chinoz tumani", callback_data="district_Chinoz tumani")],
[InlineKeyboardButton(text="Yuqorichirchiq tumani", callback_data="district_Yuqorichirchiq tumani"),
InlineKeyboardButton(text="Yangiyo‘l tuman", callback_data="district_Yangiyo‘l tuman")],
[InlineKeyboardButton(text="Ortga qaytish🔙", callback_data="district_back")]
]

k_tashkent_reg = InlineKeyboardMarkup(inline_keyboard=tashkent_reg)

fergana = [
[InlineKeyboardButton(text="Farg‘ona shahri", callback_data="district_Farg‘ona shahri"),
InlineKeyboardButton(text="Marg‘ilon shahri", callback_data="district_Marg‘ilon shahri")],
[InlineKeyboardButton(text="Quvasoy shahri", callback_data="district_Quvasoy shahri"),
InlineKeyboardButton(text="Qo‘qon shahri", callback_data="district_Qo‘qon shahri")],
[InlineKeyboardButton(text="Beshariq tumani", callback_data="district_Beshariq tumani"),
InlineKeyboardButton(text="Bog‘dod tumani", callback_data="district_Bog‘dod tumani")],
[InlineKeyboardButton(text="Buvayda tumani", callback_data="district_Buvayda tumani"),
InlineKeyboardButton(text="Dang‘ara tumani", callback_data="district_Dang‘ara tumani")],
[InlineKeyboardButton(text="Yozyovon tumani", callback_data="district_Yozyovon tumani"),
InlineKeyboardButton(text="Quva tumani", callback_data="district_Quva tumani")],
[InlineKeyboardButton(text="Qo‘shtepa tumani", callback_data="district_Qo‘shtepa tumani"),
InlineKeyboardButton(text="Oltiariq tumani", callback_data="district_Oltiariq tumani")],
[InlineKeyboardButton(text="Rishton tumani", callback_data="district_Rishton tumani"),
InlineKeyboardButton(text="So‘x tumani", callback_data="district_So‘x tumani")],
[InlineKeyboardButton(text="Toshloq tumani", callback_data="district_Toshloq tumani"),
InlineKeyboardButton(text="O‘zbekiston tumani", callback_data="district_O‘zbekiston tumani")],
[InlineKeyboardButton(text="Uchko‘prik tumani", callback_data="district_Uchko‘prik tumani"),
InlineKeyboardButton(text="Farg‘ona tumani", callback_data="district_Farg‘ona tumani")],
[InlineKeyboardButton(text="Furqat tuman", callback_data="district_Furqat tuman")],
[InlineKeyboardButton(text="Ortga qaytish🔙", callback_data="district_back")]
]

k_fergana = InlineKeyboardMarkup(inline_keyboard=fergana)

xorazm = [
[InlineKeyboardButton(text="Urganch shahri", callback_data="district_Urganch shahri"),
InlineKeyboardButton(text="Xiva shahri", callback_data="district_Xiva shahri")],
[InlineKeyboardButton(text="Bog‘ot tumani", callback_data="district_Bog‘ot tumani"),
InlineKeyboardButton(text="Gurlan tumani", callback_data="district_Gurlan tumani")],
[InlineKeyboardButton(text="Urganch tumani", callback_data="district_Urganch tumani"),
InlineKeyboardButton(text="Xiva tumani", callback_data="district_Xiva tumani")],
[InlineKeyboardButton(text="Xonqa tumani", callback_data="district_Xonqa tumani"),
InlineKeyboardButton(text="Hazorasp tumani", callback_data="district_Hazorasp tumani")],
[InlineKeyboardButton(text="Shovot tumani", callback_data="district_Shovot tumani"),
InlineKeyboardButton(text="Yangiariq tumani", callback_data="district_Yangiariq tumani")],
[InlineKeyboardButton(text="Yangibozor tumani", callback_data="district_Yangibozor tumani"),
InlineKeyboardButton(text="Qo‘shko‘pir tuman", callback_data="district_Qo‘shko‘pir tuman")],
[InlineKeyboardButton(text="Ortga qaytish🔙", callback_data="district_back")]
]

k_xorazm = InlineKeyboardMarkup(inline_keyboard=xorazm)

tashkent_city =[
[InlineKeyboardButton(text="Bektemir tumani", callback_data="district_Bektemir tumani"),
InlineKeyboardButton(text="Mirzo Ulug‘bek tumani", callback_data="district_Mirzo Ulug‘bek tumani")],
[InlineKeyboardButton(text="Mirobod tumani", callback_data="district_Mirobod tumani"),
InlineKeyboardButton(text="Olmazor tumani", callback_data="district_Olmazor tumani")],
[InlineKeyboardButton(text="Sirg‘ali tumani", callback_data="district_Sirg‘ali tumani"),
InlineKeyboardButton(text="Uchtepa tumani", callback_data="district_Uchtepa tumani")],
[InlineKeyboardButton(text="Chilonzor tumani", callback_data="district_Chilonzor tumani"),
InlineKeyboardButton(text="Shayxontohur tumani", callback_data="district_Shayxontohur tumani")],
[InlineKeyboardButton(text="Yunusobod tumani", callback_data="district_Yunusobod tumani"),
InlineKeyboardButton(text="Yakkasaroy tumani", callback_data="district_Yakkasaroy tumani")],
[InlineKeyboardButton(text="Yashnobod tuman", callback_data="district_Yashnobod tuman")],
[InlineKeyboardButton(text="Ortga qaytish🔙", callback_data="district_back")]
]

k_tashkent_city = InlineKeyboardMarkup(inline_keyboard=tashkent_city)

regions = [
[InlineKeyboardButton(text="Andijon viloyati", callback_data="region_Andijon viloyati"),
InlineKeyboardButton(text="Buxoro viloyati", callback_data="region_Buxoro viloyati")],
[InlineKeyboardButton(text="Fargʻona viloyati", callback_data="region_Fargʻona viloyati"),
InlineKeyboardButton(text="Jizzax viloyati", callback_data="region_Jizzax viloyati")],
[InlineKeyboardButton(text="Xorazm viloyati", callback_data="region_Xorazm viloyati"),
InlineKeyboardButton(text="Namangan viloyati", callback_data="region_Namangan viloyati")],
[InlineKeyboardButton(text="Navoiy viloyati", callback_data="region_Navoiy viloyati"),
InlineKeyboardButton(text="Qashqadaryo viloyati", callback_data="region_Qashqadaryo viloyati")],
[InlineKeyboardButton(text="Qoraqalpogʻiston Respublikasi", callback_data="region_Qoraqalpogʻiston Respublikasi"),
InlineKeyboardButton(text="Samarqand viloyati", callback_data="region_Samarqand viloyati")],
[InlineKeyboardButton(text="Sirdaryo viloyati", callback_data="region_Sirdaryo viloyati"),
InlineKeyboardButton(text="Surxondaryo viloyati", callback_data="region_Surxondaryo viloyati")],
[InlineKeyboardButton(text="Toshkent viloyati", callback_data="region_Toshkent viloyati"),
InlineKeyboardButton(text="Toshkent shahri", callback_data="region_Toshkent shahri")],
[InlineKeyboardButton(text="Ortga qaytish🔙", callback_data="region_back")]
]

k_regions =InlineKeyboardMarkup(inline_keyboard=regions)


select_subject_degree =[
[InlineKeyboardButton(text="1 chi fan", callback_data="first_subject")],
[InlineKeyboardButton(text="2 chi fan", callback_data="second_subject")],
[InlineKeyboardButton(text="Ortga qaytish🔙", callback_data="detect_back")]
]

k_select_subject_degree= InlineKeyboardMarkup(inline_keyboard=select_subject_degree)
