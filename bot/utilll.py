import re
keyboard = ''
text = """
<li>Bektemir tumani</li> 
<li>Mirzo Ulug‘bek tumani</li> 
<li>Mirobod tumani</li> 
<li>Olmazor tumani</li> 
<li>Sirg‘ali tumani</li> 
<li>Uchtepa tumani</li> 
<li>Chilonzor tumani</li> 
<li>Shayxontohur tumani</li> 
<li>Yunusobod tumani</li> 
<li>Yakkasaroy tumani</li> 
<li>Yashnobod tumani</li>
"""

g = re.findall(r"<li>.+", text, re.MULTILINE)
inf = 1
for i in g:
    if inf == 1:
        print(f'[InlineKeyboardButton(text="{i[4:][:-6]}", callback_data="district_{i[4:][:-6]}"),')
        inf+=1
    elif inf == 2:
        print(f'InlineKeyboardButton(text="{i[4:][:-6]}", callback_data="district_{i[4:][:-6]}")],')
        inf=1