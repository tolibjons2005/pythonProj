import pdfkit
import jinja2

import time

from db.user import get_n_test
from pdftool.create_qr import create_qr_fo
from io import BytesIO

start_time = time.time()

path_to_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'


context = {
           #  'first_sub':first_sub,
           # 'second_sub':second_sub,
           # 'third_sub':third_sub,
           # 'name':namea,
           # 'name_s':name_s,
           # 'id':id1,
           # 'date':date1,
           # 'block1':"block1",
           # 'block2':block2,
           # 'block3':block3
}


config = pdfkit.configuration()
template_loader = jinja2.FileSystemLoader('./')
template_env=jinja2.Environment(loader=template_loader)


async def create_title_on(tid, name_s, date, channel_link, second_sub, third_sub, test_type, t_sub):


    code = ''
    if test_type == '90':
        css_path = "./pdftool/template/title_template.css"
        template = template_env.get_template('./pdftool/template/title_template.html')


        await create_qr_fo(tid, test_type=test_type)

        code += f"""<div class="up_block">
               <div class="list_of_data">
                   <img class='qr' src="file:////root/cardbot/pythonProject/bot/pdftool/qrcodes/channel_link/t_id{tid}.png" alt="Girl in a jacket" width="234px" height="234px">
                   <span class="bold">MUASSASA NOMI: </span>{name_s}</br>
                   <span class="bold">BUYURTMA SANASI: </span>{date}</br>
                   <span class="bold">MUALLIF KANALI: </span>{channel_link}

                   <div style="width:600px; margin-top:100px;" class="name"><hr style="border: 1px solid black;"></div>

               </div>
               <table class="subject_name"><tr >
               <td style="text-align:right; padding-right:40px; width:322px;  "><span class='bold'>Majburiy fanlar </span>(1.1)</td>
               <td style="text-align:right; padding-right:40px; width:322px; "><span class='bold'>{second_sub} </span>(3.1)</td>
               <td style="text-align:right; padding-right:40px; width:322px;"><span class='bold'>{third_sub} </span>(2.1)</td>
           </tr></table>


           </div>


           <img class="title" src="file:////root/cardbot/pythonProject/bot/pdftool/template/title.png" alt="Girl in a jacket" width="968px" height="1288px">
           """
        margin_bottom = '0px'
    elif test_type == '30':
        css_path = "./pdftool/template/title_template30.css"
        template = template_env.get_template('./pdftool/template/title_template30.html')


        await create_qr_fo(tid, test_type=test_type)
        code += f"""
            <div class="up_block">
        <div class="list_of_data">
            <img class='qr' src="file:////root/cardbot/pythonProject/bot/pdftool/qrcodes/channel_link/t_id{tid}.png" alt="Girl in a jacket" width="234px" height="234px">
            <span class="bold">MUASSASA NOMI: </span>{name_s}</br>
            <span class="bold">BUYURTMA SANASI: </span>{date}</br>
            <span class="bold">MUALLIF KANALI: </span>{channel_link}</br>
            <span class="bold">FAN NOMI: </span>{t_sub}

            <div style="width:600px; margin-top:60px; " ><hr style="border: 1px solid black;"></div>


        </div>
        <img class="title" src="file:////root/cardbot/pythonProject/bot/pdftool/template/hj.png" alt="Girl in a jacket" width="968px" height="488px">
        </div>
        """

        margin_bottom = '35px'




    context['code']=code
    output_text = template.render(context)

    options = {
        # 'quiet': '',
        # 'javascript-delay' : '2000',
        # 'page-size': 'A4',
        'page-width': '1190px',
        'page-height': '1684px',

        'margin-top': '40px',
        'margin-right': '1px',
        'margin-bottom': margin_bottom,
        'margin-left': '1px',
        'zoom': 1,
        # 'no-outline': '',
        'disable-smart-shrinking': True,
        'enable-local-file-access': ''
        # 'disable-local-file-access': ''

    }

    title_io=pdfkit.from_string(output_text, options=options, configuration=config, css=css_path)
    return title_io

