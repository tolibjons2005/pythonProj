import os
import shutil
import fitz
import pdfkit
import jinja2
import PyPDF2
from db.user import add_to_ONLINE
from pdftool.docx2string import get_string, get_str
from pdftool.create_qr import create_qr_fo
import time
import asyncio

start_time = time.time()

from io import BytesIO

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

config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)
template_loader = jinja2.FileSystemLoader('./')
template_env = jinja2.Environment(loader=template_loader)


async def create_pdf_on(output_file, test_type, second_sub, third_sub,expire_date, date, tid, session_maker, t_sub, channel_link,name_s):
    parent_dir = "D:/pythonProject/bot/img"
    directory = f"id{tid}"

    # Path
    path = os.path.join(parent_dir, directory)
    os.makedirs(path)

    text1 = get_str(tid, output_file)
    output_file.close()

    i = 0
    func_string = ""
    tests = ''

    await create_qr_fo(tid, channel_name=channel_link)

    if test_type == '30':
        try:

            text, answ = get_string(text1, test_type, second_sub, third_sub, t_sub)
        except IndexError as e:
            shutil.rmtree(path)
            raise


        await add_to_ONLINE(tid, answ, expire_date, session_maker)
        template = template_env.get_template('./pdftool/template/template_for_online.html')

        func_string += f"""
        $(function(){{
        var content_height = 1048;	// the height of the content, discluding the header/footer
        var page = 1;



       function buildNewsletter1{i}(){{

            if($('#newsletterContent1{i}').contents().length > 0 ){{
                // when we need to add a new page, use a jq object for a template
                // or use a long HTML string, whatever your preference
                $page = $("#page_template").clone().addClass("page").css("display", "block");

                // fun stuff, like adding page numbers to the footer
                $page.find(".footer span").append(page);
                
                page++;
                $("body").append($page);



                // here is the columnizer magic
                $('#newsletterContent1{i}').columnize({{
                    columns:2,

                    target: ".page:last .content",
                    overflow: {{
                        height: content_height,
                        id: "#newsletterContent1{i}",
                        doneFunc: function(){{
                            console.log(page);

                            buildNewsletter1{i}();}}



                    }}
                }});




            }}
        }}
        setTimeout(buildNewsletter1{i}, 200);


        function buildNewsletterrr4{i}(){{

        if ((0!=((page-1)%4)) && (page-1) != 2){{

        for(var i = 0; i < (4-((page-1)%4)); i++){{

         $blank_page=$("#blankkk").clone().css("display", "block");

        $('body').append($blank_page);
        }}
                                }}

        }}setTimeout(buildNewsletterrr4{i}, 200);





        }});


"""
        tests += f"""
        <div id="newsletterContent1{i}">{text}</div>

"""
        context['functions'] = func_string
        context['tests'] = tests
        context['name_s'] = name_s
        context['channel_link'] = channel_link
        context['teacher_id'] = '30'+str(tid)

        context['date'] = date
        p_height = '1188px'


        delay = 2500
    else:
        rown = False
        rown2 = False
        if second_sub in ['Kimyo']:
            row_2 = 1
            rown = True
        else:
            row_2 = 2

        if third_sub in ['Kimyo']:
            row_3 = 1
            rown2 = True
        else:
            row_3 = 2


        try:

            text, answ = get_string(text1, test_type, second_sub, third_sub, rown, rown2)
        except IndexError as e:
            shutil.rmtree(path)
            raise



        await add_to_ONLINE(tid, answ, expire_date, session_maker, subject_1=second_sub, subject_2=third_sub)

        func_string += f"""
        $(function(){{
        var content_height = 1048;	// the height of the content, discluding the header/footer
        var page = 2;

        function buildNewsletterrr5{i}(){{
        $cover= $('#cover1').clone()
        
        $("body").append($cover.css("display", "block"));

        }}setTimeout(buildNewsletterrr5{i}, 100);

       function buildNewsletter1{i}(){{

            if($('#newsletterContent1{i}').contents().length > 0 ){{
                // when we need to add a new page, use a jq object for a template
                // or use a long HTML string, whatever your preference
                $page = $("#page_template").clone().addClass("page").css("display", "block");

                // fun stuff, like adding page numbers to the footer
                $page.find(".footer span").append(page);
                
                page++;
                $("body").append($page);



                // here is the columnizer magic
                $('#newsletterContent1{i}').columnize({{
                    columns:2,

                    target: ".page:last .content",
                    overflow: {{
                        height: content_height,
                        id: "#newsletterContent1{i}",
                        doneFunc: function(){{
                            console.log(page);

                            buildNewsletter1{i}();}}



                    }}
                }});




            }}
        }}
        setTimeout(buildNewsletter1{i}, 100);

        function buildNewsletterr2{i}(){{
            if($('#test2{i}').contents().length > 0 ){{
                // when we need to add a new page, use a jq object for a template
                // or use a long HTML string, whatever your preference
                $page = $("#page_template").clone().addClass("page").css("display", "block");

                // fun stuff, like adding page numbers to the footer
                $page.find(".footer span").append(page);
                
                page++;

                $("body").append($page);


                // here is the columnizer magic
                $('#test2{i}').columnize({{
                    columns:{row_2},

                    target: ".page:last .content",
                    overflow: {{
                        height: content_height,
                        id: "#test2{i}",
                        doneFunc: function(){{
                            console.log("done with page");
                            buildNewsletterr2{i}();
                        }}
                    }}
                }});




            }}
        }}
        setTimeout(buildNewsletterr2{i}, 100);

        function buildNewsletterrr3{i}(){{

            if($('#test3{i}').contents().length > 0 ){{

                // when we need to add a new page, use a jq object for a template
                // or use a long HTML string, whatever your preference
                $page = $("#page_template").clone().addClass("page").css("display", "block");

                // fun stuff, like adding page numbers to the footer
                $page.find(".footer span").append(page);
                
                page++;
                $("body").append($page);



                // here is the columnizer magic
                $('#test3{i}').columnize({{
                    columns:{row_3},

                    target: ".page:last .content",
                    overflow: {{
                        height: content_height,
                        id: "#test3{i}",
                        doneFunc: function(){{
                            console.log("done with page");


                            buildNewsletterrr3{i}();




                        }}

                    }}
                }});





            }}
        }}
        setTimeout(buildNewsletterrr3{i}, 100);

        function buildNewsletterrr4{i}(){{
        if (0!=((page-1)%4)) {{

        for(var i = 0; i < (4-((page-1)%4)); i++){{

         $blank_page=$("#blankkk").clone().css("display", "block");

        $('body').append($blank_page);
        }}
                                }}

        }}setTimeout(buildNewsletterrr4{i}, 100);
        }});
        """

        tests += f"""
        <div id="newsletterContent1{i}">{text[0]}</div>
        <div id="test2{i}">{text[1]}</div>
        <div id="test3{i}">{text[2]}</div>
                    """

        template = template_env.get_template('./pdftool/template/template_for_online90.html')

        context['functions'] = func_string
        context['first_sub'] = 'Majburiy fanlar'
        context['second_sub'] = second_sub
        context['third_sub'] = third_sub
        context['teacher_id'] = '90'+str(tid)
        context['channel_link'] = channel_link

        context['name_s'] = name_s

        context['date'] = date

        context['tests'] = tests
        p_height='1189px'
        delay = 2500

    output_text = template.render(context)

    options = {

        'javascript-delay': delay,

        'page-width': '840px',
        'page-height': p_height,

        'margin-top': '0px',
        'margin-right': '1px',
        'margin-bottom': '0px',
        'margin-left': '1px',
        'zoom': 1,
        'no-outline': '',
        'disable-smart-shrinking': True,
        'enable-local-file-access': '',
        'debug-javascript': '',


    }

    save_to_io = pdfkit.from_string(output_text, options=options, configuration=config,
                                    css="./pdftool/template/template.css")





    shutil.rmtree(path)
    return save_to_io