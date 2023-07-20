import os
import shutil

import pdfkit
import jinja2
import PyPDF2
from db.user import add_answers
from pdftool.docx2string import get_string, get_str
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


config = pdfkit.configuration()
template_loader = jinja2.FileSystemLoader('./')
template_env=jinja2.Environment(loader=template_loader)



async def create_pdf(output_file, test_type, second_sub, third_sub, name_s, ids, date, tid, session_maker, t_sub, book_type):
    parent_dir = "/root/cardbot/pythonProject/bot/img"
    directory = f"id{tid}"

    # Path
    path = os.path.join(parent_dir, directory)
    os.makedirs(path)

    text1 = get_str(tid,output_file)

    i= 0
    func_string = ""
    tests =''
    output_file.close()

    if test_type == '30':
        for k in ids:
            try:
                text, answ = get_string(text1, test_type, second_sub, third_sub, t_sub)
            except IndexError as e:
                shutil.rmtree(path)
                raise
                break
            i += 1
            id = k.student_id
            name = k.st_fullname
            await add_answers(k.student_id,tid, answ, test_type, session_maker)
            template = template_env.get_template('./pdftool/template/template30.html')

            func_string+=f"""
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
					$page.find(".header .name_class").append("{name}");
					$page.find(".header .id_class").append("{id}");
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
        context['tests'] = tests.replace('\\frac','\\dfrac')
        context['name_s'] = name_s

        context['date'] = date
        p_height = '1188px'

        # template = template_env.get_template('./pdftool/template/templatecopy.html')
        # context['block1'] = get_string(output_file, test_type)
        delay= 2500*len(ids)
    else:
        rown = False
        rown2 = False
        if second_sub in ['Kimyo', 'Matematika','Fizika']:
            row_2 = 1
            rown = True
            for_second_html='large'
        else:
            row_2=2
            for_second_html = 'small'



        if third_sub in ['Kimyo', 'Matematika','Fizika']:
            row_3=1
            rown2 = True
            for_third_html = 'large'
        else:
            row_3=2
            for_third_html = 'small'






        for k in ids:
            try:

                text,answ = get_string(text1, test_type, second_sub, third_sub, rown, rown2 )
            except IndexError as e:
                shutil.rmtree(path)
                raise
                break
            # print('TOLIBJON')
            i += 1
            id = k.student_id
            name = k.st_fullname
            await add_answers(k.student_id,tid,answ, test_type, session_maker)



            func_string += f"""
            $(function(){{
			var content_height = 1048;	// the height of the content, discluding the header/footer
			var page = 2;
			
			function buildNewsletterrr5{i}(){{
			$cover= $('#cover1').clone()
			$cover.find(".id_classs").append("{id}")
			$cover.find(".namn").append("{name}")
			$("body").append($cover.css("display", "block"));
			
			}}setTimeout(buildNewsletterrr5{i}, 100);
			
           function buildNewsletter1{i}(){{
           
				if($('#newsletterContent1{i}').contents().length > 0 ){{
					// when we need to add a new page, use a jq object for a template
					// or use a long HTML string, whatever your preference
					$page = $("#page_template").clone().addClass("page").css("display", "block");

					// fun stuff, like adding page numbers to the footer
					$page.find(".footer span").append(page);
					$page.find(".header .name_class").append("{name}");
					$page.find(".header .id_class").append("{id}");
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
					$page.find(".header .name_class").append("{name}");
					$page.find(".header .id_class").append("{id}");
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
					$page.find(".header .name_class").append("{name}");
					$page.find(".header .id_class").append("{id}");
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
            <div id="test2{i}" class="{for_second_html}">{text[1]}</div>
            <div id="test3{i}" class="{for_third_html}">{text[2]}</div>
                        """

        template = template_env.get_template('./pdftool/template/template.html')

        context['functions']=func_string
        context['first_sub']='Majburiy fanlar'
        context['second_sub']=second_sub
        context['third_sub']=third_sub

        context['name_s']=name_s

        context['date']=date

        context['tests'] = tests.replace('\\frac', '\\dfrac')
        p_height = '1189px'
        delay= 5000*len(ids)



    output_text = template.render(context)
    ism = "Komiljonov Tolibjon"
    id = "20050617"
    options = {
        # 'quiet': '',
        'javascript-delay': delay,
        # 'page-size': 'A4',
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
        #'debug-javascript':'',
        #'no-stop-slow-scipts':''
        # 'disable-local-file-access': ''

    }
    # print("--- %s seconds ---" % (time.time() - start_time))
    # pdfkit.from_string(output_text, output_path=f"{n}", options=options, configuration=config,
    #                    css="template/template.css")

    save_to_io = pdfkit.from_string(output_text,  options=options, configuration=config, css="./pdftool/template/template.css")

    # print("--- %s seconds ---" % (time.time() - start_time))


    if test_type =='90':
        if book_type == '2':
            bytesio = BytesIO(save_to_io)
            print(book_type)

            pdf_document =PyPDF2.PdfReader(bytesio)
            pn = len(pdf_document.pages)
            sn = len(ids)
            vbc = sn

            pceb = int(pn / sn)
            new_pceb = pn / sn
            print(pceb % 4)
            if new_pceb % 4 == 0:

                cover_list = []
                inner_list = []
                covers = f'1-{int(pn / 2)}'
                inners = f'{int(pn / 2) + 1}-{pn}'

                for i in range(1, sn + 1):

                    pneb = (pceb * i) - 1
                    spneb = pneb + 1 - pceb
                    # bseb = pneb - int(pceb / 2)
                    # beeb = bseb + 1
                    bseb = (pceb * vbc - int(pceb / 2)) - 1
                    beeb = bseb + 1
                    vbc = vbc - 1

                    while True:

                        # cover_list += f"{pneb},{spneb},"

                        #

                        cover_list.append(pneb)
                        cover_list.append(spneb)
                        inner_list.append(bseb)
                        inner_list.append(beeb)

                        if (pneb - spneb) == 3:
                            break
                        pneb = pneb - 2
                        spneb += 2
                        bseb = bseb - 2
                        beeb += 2
            else:
                context['tests'] = tests.replace('dontsplit', '')
                print(tests)
                delay = '5000'
                output_text = template.render(context)
                options = {
                    # 'quiet': '',
                    'javascript-delay': delay,
                    # 'page-size': 'A4',
                    'page-width': '840px',
                    'page-height': '1189px',

                    'margin-top': '0px',
                    'margin-right': '1px',
                    'margin-bottom': '0px',
                    'margin-left': '1px',
                    'zoom': 1,
                    'no-outline': '',
                    'disable-smart-shrinking': True,
                    'enable-local-file-access': '',
                    'debug-javascript': '',
                    # 'no-stop-slow-scipts':''
                    # 'disable-local-file-access': ''

                }
                # print("--- %s seconds ---" % (time.time() - start_time))
                # pdfkit.from_string(output_text, output_path=f"{n}", options=options, configuration=config,
                #                    css="template/template.css")

                save_to_io = pdfkit.from_string(output_text, options=options, configuration=config,
                                                css="./pdftool/template/template.css")

                bytesio = BytesIO(save_to_io)

                pdf_document = PyPDF2.PdfReader(bytesio)
                pn = len(pdf_document.pages)
                sn = len(ids)
                vbc = sn

                pceb = int(pn / sn)
                cover_list = []
                inner_list = []
                covers = f'1-{int(pn / 2)}'
                inners = f'{int(pn / 2) + 1}-{pn}'

                for i in range(1, sn + 1):

                    pneb = (pceb * i) - 1
                    spneb = pneb + 1 - pceb
                    # bseb = pneb - int(pceb / 2)
                    # beeb = bseb + 1
                    bseb = (pceb * vbc - int(pceb / 2)) - 1
                    beeb = bseb + 1
                    vbc = vbc - 1
                    while True:

                        # cover_list += f"{pneb},{spneb},"
                        #

                        cover_list.append(pneb)
                        cover_list.append(spneb)
                        inner_list.append(bseb)
                        inner_list.append(beeb)

                        if (pneb - spneb) == 3:
                            break
                        pneb = pneb - 2
                        spneb += 2
                        bseb = bseb - 2
                        beeb += 2
            writer = PyPDF2.PdfWriter()
            page_order = cover_list + inner_list
            for page_number in page_order:
                page = pdf_document.pages[page_number]
                writer.add_page(page)
            writer.write(bytesio)

            writer.close()
            save_to_io = bytesio.getvalue()
            bytesio.close()



        else:
            covers = 'over'
            inners = ' over'
    else:
        if book_type == '2':
            cover_list = []
            inner_list = []
            print(book_type)
            bytesio = BytesIO(save_to_io)


            pdf_document = PyPDF2.PdfReader(bytesio)
            pn = len(pdf_document.pages)
            sn = len(ids)
            vbc = sn

            pceb = int(pn / sn)
            new_pceb = pn / sn
            print(pceb % 4)
            if new_pceb==2:
                start_page= 1
                covers = f'1-{int(pn / 2)}'
                inners = f'{int(pn / 2) + 1}-{pn}'

                for i in range(1, int(sn/2) + 1):
                    cover_list.append(start_page-1)
                    cover_list.append(start_page + 1)
                    inner_list.append(pn-1)
                    inner_list.append(pn - 3)
                    start_page=start_page+4
                    pn=pn-4
            elif new_pceb % 4 == 0:

                cover_list = []
                inner_list = []
                covers = f'1-{int(pn / 2)}'
                inners = f'{int(pn / 2) + 1}-{pn}'

                for i in range(1, sn + 1):

                    pneb = (pceb * i)-1
                    spneb = pneb +1- pceb
                    # bseb = pneb - int(pceb / 2)
                    # beeb = bseb + 1
                    bseb = (pceb * vbc - int(pceb / 2))-1
                    beeb = bseb + 1
                    vbc = vbc - 1
                    while True:


                            # cover_list += f"{pneb},{spneb},"
                            #

                        cover_list.append(pneb)
                        cover_list.append(spneb)
                        inner_list.append(bseb)
                        inner_list.append(beeb)


                        if (pneb - spneb) == 3:
                            print(inner_list)
                            break
                        pneb = pneb - 2
                        spneb += 2
                        bseb = bseb - 2
                        beeb += 2
            else:
                context['tests'] = tests.replace('dontsplit', '')
                print(tests)
                delay = '5000'
                output_text = template.render(context)

                options = {
                    # 'quiet': '',
                    'javascript-delay': delay,
                    # 'page-size': 'A4',
                    'page-width': '840px',
                    'page-height': '1188px',

                    'margin-top': '0px',
                    'margin-right': '1px',
                    'margin-bottom': '0px',
                    'margin-left': '1px',
                    'zoom': 1,
                    'no-outline': '',
                    'disable-smart-shrinking': True,
                    'enable-local-file-access': '',
                    'debug-javascript': '',
                    # 'no-stop-slow-scipts':''
                    # 'disable-local-file-access': ''

                }
                # print("--- %s seconds ---" % (time.time() - start_time))
                # pdfkit.from_string(output_text, output_path=f"{n}", options=options, configuration=config,
                #                    css="template/template.css")

                save_to_io = pdfkit.from_string(output_text, options=options, configuration=config,
                                                css="./pdftool/template/template.css")
                bytesio = BytesIO(save_to_io)

                pdf_document = PyPDF2.PdfReader(bytesio)
                pn = len(pdf_document.pages)
                sn = len(ids)
                vbc = sn

                pceb = int(pn / sn)
                cover_list = []
                inner_list = []
                covers = f'1-{int(pn / 2)}'
                inners = f'{int(pn / 2) + 1}-{pn}'

                for i in range(1, sn + 1):

                    pneb = (pceb * i) - 1
                    spneb = pneb + 1 - pceb
                    # bseb = pneb - int(pceb / 2)
                    # beeb = bseb + 1
                    bseb = (pceb * vbc - int(pceb / 2)) - 1
                    beeb = bseb + 1
                    vbc = vbc - 1
                    while True:

                        # cover_list += f"{pneb},{spneb},"
                        #

                        cover_list.append(pneb)
                        cover_list.append(spneb)
                        inner_list.append(bseb)
                        inner_list.append(beeb)

                        if (pneb - spneb) == 3:
                            break
                        pneb = pneb - 2
                        spneb += 2
                        bseb = bseb - 2
                        beeb += 2
            writer = PyPDF2.PdfWriter()
            page_order = cover_list + inner_list
            for page_number in page_order:
                page = pdf_document.pages[page_number]
                writer.add_page(page)
            writer.write(bytesio)

            writer.close()
            save_to_io = bytesio.getvalue()
            bytesio.close()





        else:
            covers = 'over'
            inners = ' over'


    shutil.rmtree(path)
    return save_to_io, covers, inners














