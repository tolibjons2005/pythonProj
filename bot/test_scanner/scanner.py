from functools import wraps

import cv2
import numpy as np
import test_scanner.scanner_f as sf
import io
from pyzbar.pyzbar import decode

from db.user import get_st_answ, add_score, add_ans_message
from aiogram import html
from numba import njit
from memory_profiler import profile
def memoize(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key=str(args)+str(kwargs)

        if key not in cache:
            cache[key]=func(*args, **kwargs)

        return cache[key]

    return wrapper

async def test_scanner_func(imgg, session_maker, teacher_id):
    ###################################
    # path = 'images/img_10.png'
    # img = cv2.imread(imgg)

    img = cv2.imdecode(np.frombuffer(imgg.read(), np.uint8), 1)

    code = decode(img)
    # cv2.imshow('gh', img)
    print(code)
    if code == []:
        imgQRGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imTH=cv2.adaptiveThreshold(imgQRGray,
                              255,  # maximum value assigned to pixel values exceeding the threshold
                              cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # gaussian weighted sum of neighborhood
                              cv2.THRESH_BINARY,  # thresholding type
                              53,  # block size (5x5 window)
                              5)
        # cv2.imshow('h',imTH)
        code = decode(imTH)

        # cv2.waitKey(0);
        # cv2.destroyAllWindows();
        # cv2.waitKey(1)

    userid = code[0].data.decode('utf-8')
    print(userid)
    id = userid[2:-1]
    test_type =  userid[0:2]
    data = await get_st_answ(int(id), teacher_id,test_type, session_maker)

    fullname = data.st_fullname
    second_s = data.subject_1
    third_s = data.subject_2
    if test_type =='90':
        ans = data.st_answers90
        imgWidth = 960
        imgHeight = 1280

        questions = 30
    elif test_type == '30':
        ans = data.st_answers30
        imgWidth = 960
        imgHeight = 480

        questions = 10


    if ans =='8':
        grading=' '
        resultg = 'Ushbu test tekshirilgan'
        h, w, c = img.shape

        if code[0].orientation == 'UP':
            start_x = code[0].polygon[0].x
            end_x = code[0].polygon[2].x
            end_y = code[0].polygon[2].y
            start_y = 0
            start_point = (start_x, start_y)
            end_point = (end_x, end_y)
            color = (255, 255, 255)
            thickness = -1
            img = cv2.rectangle(img, start_point, end_point, color, thickness)
        elif code[0].orientation == 'LEFT':

            start_x = 0
            end_x = code[0].polygon[3].x
            end_y = code[0].polygon[3].y
            start_y = code[0].polygon[1].y
            start_point = (start_x, start_y)
            end_point = (end_x, end_y)
            color = (255, 255, 255)
            thickness = -1

            img = cv2.rectangle(img, start_point, end_point, color, thickness)
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        elif code[0].orientation == 'RIGHT':

            start_x = w
            end_x = code[0].polygon[1].x
            end_y = code[0].polygon[1].y
            start_y = code[0].polygon[3].y
            start_point = (start_x, start_y)
            end_point = (end_x, end_y)
            color = (255, 255, 255)
            thickness = -1

            img = cv2.rectangle(img, start_point, end_point, color, thickness)
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif code[0].orientation == 'DOWN':

            start_x = code[0].polygon[2].x
            end_x = code[0].polygon[0].x
            end_y = code[0].polygon[0].y
            start_y = h
            start_point = (start_x, start_y)
            end_point = (end_x, end_y)
            color = (255, 255, 255)
            thickness = -1
            img = cv2.rectangle(img, start_point, end_point, color, thickness)
            img = cv2.rotate(img, cv2.ROTATE_180)

        code = decode(img)
        # cv2.imshow('ghh',img)
        # cv2.waitKey(0);
        # cv2.destroyAllWindows();
        # cv2.waitKey(1)
        return resultg
    else:
        # Using cv2.rectangle() method
        # Draw a rectangle of black color of thickness -1 px

        # img = cv2.resize(img, (1000, 1000))
        h, w, c = img.shape

        if code[0].orientation == 'UP':
            start_x = code[0].polygon[0].x
            end_x = code[0].polygon[2].x
            end_y = code[0].polygon[2].y
            start_y = 0
            start_point = (start_x, start_y)
            end_point = (end_x, end_y)
            color = (255, 255, 255)
            thickness = -1
            img = cv2.rectangle(img, start_point, end_point, color, thickness)
        elif code[0].orientation == 'LEFT':

            start_x = 0
            end_x = code[0].polygon[3].x
            end_y = code[0].polygon[3].y
            start_y = code[0].polygon[1].y
            start_point = (start_x, start_y)
            end_point = (end_x, end_y)
            color = (255, 255, 255)
            thickness = -1

            img = cv2.rectangle(img, start_point, end_point, color, thickness)
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        elif code[0].orientation == 'RIGHT':

            start_x = w
            end_x = code[0].polygon[0].x
            end_y = code[0].polygon[0].y
            start_y = code[0].polygon[3].y
            start_point = (start_x, start_y)
            end_point = (end_x, end_y)
            color = (255, 255, 255)
            thickness = -1

            img = cv2.rectangle(img, start_point, end_point, color, thickness)
            img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        elif code[0].orientation == 'DOWN':

            start_x = code[0].polygon[2].x
            end_x = code[0].polygon[0].x
            end_y = code[0].polygon[0].y
            start_y = h
            start_point = (start_x, start_y)
            end_point = (end_x, end_y)
            color = (255, 255, 255)
            thickness = -1
            img = cv2.rectangle(img, start_point, end_point, color, thickness)
            img = cv2.rotate(img, cv2.ROTATE_180)



        # code = decode(img)
        # cv2.imshow('ghh',img)
        #
        # cv2.waitKey(0);
        # cv2.destroyAllWindows();
        # cv2.waitKey(1)




        # cv2.imshow('dfs', img)
        collums = 3
        choices = 5


        ###########################################
        # img =cv2.resize(img, (1000,1000))
        imgContours = img.copy()
        imgBiggestContours = img.copy()

        imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (19, 19), 1)
        # cv2.imshow("Reslt", imgBlur)
        imgCanny = sf.auto_canny(imgBlur)
        # cv2.imshow("Relt", imgCanny)

        contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(imgContours, contours, -1, (0, 255, 5), 10)

        imgBlank = np.zeros_like(img)

        rectCon = sf.rectContour(contours)
        biggestContour = sf.getCornerPoints(rectCon[0])
        # gradePoints = sf.getCornerPoints(rectCon[1])
        print(biggestContour)

        if biggestContour.size != 0:
            cv2.drawContours(imgBiggestContours, biggestContour, -1, (0, 255, 5), 20)
            # cv2.drawContours(imgBiggestContours, gradePoints,-1, (255,0,0),20)

            biggestContour = sf.reorder(biggestContour)
            # gradePoints = sf.reorder(gradePoints)

            pt1 = np.float32(biggestContour)
            pt2 = np.float32([[0, 0], [imgWidth, 0], [0, imgHeight], [imgWidth, imgHeight]])
            matrix = cv2.getPerspectiveTransform(pt1, pt2)
            imgWarpColored = cv2.warpPerspective(img, matrix, (imgWidth, imgHeight))

            # ptG1 = np.float32(gradePoints)
            # ptG2 = np.float32([[0, 0], [325, 0], [0, 150], [325, 150]])
            # matrixG = cv2.getPerspectiveTransform(ptG1, ptG2)
            # imgGradeDisplay = cv2.warpPerspective(img, matrixG, (325, 150))

            # cv2.imshow("Rt",imgGradeDisplay)

            imgWarpGray = cv2.cvtColor(imgWarpColored, cv2.COLOR_BGR2GRAY)
            imgThresh = cv2.adaptiveThreshold(imgWarpGray,
                                              255,  # maximum value assigned to pixel values exceeding the threshold
                                              cv2.ADAPTIVE_THRESH_GAUSSIAN_C,  # gaussian weighted sum of neighborhood
                                              cv2.THRESH_BINARY_INV,  # thresholding type
                                              41,  # block size (5x5 window)
                                              21)

            boxes = sf.splitBoxes(imgThresh, questions)
            # cv2.imshow("imgThresh",boxes[10])
            # print(cv2.countNonZero(boxes[1]))

            myPixelVal = np.zeros((collums, questions, choices))
            countC = 0
            countR = 0
            countCo = 0

            for image in boxes:
                totalPixels = cv2.countNonZero(image)
                myPixelVal[countCo][countR][countC] = totalPixels
                countC += 1
                if (countC == choices): countR += 1;countC = 0
                if (countR == questions): countCo += 1;countR = 0

            print(myPixelVal)

            myIndex = [[],
                       [],
                       []]

            countCnew = 0

            print(type(len(myPixelVal[0])))
            print("---------sfgsf-----", np.amax(myPixelVal))
            max_val = np.amax(myPixelVal) - 250.0
            if max_val > (np.amax(np.amin(np.amax(myPixelVal, axis=2), axis=1))):
                max_val = 1000.0
            else:
                pass

            for x in range(0, len(myPixelVal[0])):
                arr = myPixelVal[0][x]
                print("--------------", np.amax(arr))
                checker = np.where(arr >= max_val)
                if len(checker[0]) > 1:
                    myIndex[0].append(5)
                elif len(checker[0]) == 0:
                    myIndex[0].append(0)
                else:
                    myIndexVal = np.where(arr == np.amax(arr))
                    myIndex[0].append(myIndexVal[0][0])

            for x in range(0, len(myPixelVal[1])):
                arr = myPixelVal[1][x]
                print("--------------", np.amax(arr))
                checker = np.where(arr >= max_val)
                if len(checker[0]) > 1:
                    myIndex[1].append(5)
                elif len(checker[0]) == 0:
                    myIndex[1].append(0)
                else:
                    myIndexVal = np.where(arr == np.amax(arr))
                    myIndex[1].append(myIndexVal[0][0])

            for x in range(0, len(myPixelVal[2])):
                arr = myPixelVal[2][x]
                print("--------------", np.amax(arr) - 10.0)
                checker = np.where(arr >= max_val)
                if len(checker[0]) > 1:
                    myIndex[2].append(5)
                elif len(checker[0]) == 0:
                    myIndex[2].append(0)
                else:
                    myIndexVal = np.where(arr == np.amax(arr))
                    myIndex[2].append(myIndexVal[0][0])

            print(myIndex)

            # oxes = sf.splitoxes(imgThresh)
            # print(oxes[1])
            # cv2.imshow('sd',boxes[0])
            # ans = [[], [], []]
            # for x in range(0, 30):
            #     ans[0].append(1)
            #     ans[1].append(1)
            #     ans[2].append(1)
            #
            # ans[0][1] = 2
            # ans[0][2] = 3
            # ans[1][0] = 1
            # ans[1][1] = 2
            # ans[1][2] = 4

            # grading = [[], [], []]
            # co = 0
            # ro = 0
            # print(ans)
            # for x in range(0, 90):
            #     if ans[ro][co] == myIndex[ro][co]:
            #         grading[ro].append(1)
            #     elif myIndex[ro][co] == 5:
            #         grading[ro].append(2)
            #     else:
            #         grading[ro].append(0)
            #     co += 1
            #     if (co == 30): ro += 1;co = 0
            # print(grading)
            # print(type(code[0].orientation))

        from platform import python_version
        # imageArray = (
        #     [imgContours, imgCanny, imgThresh, imgBiggestContours])
        #
        # imgStacked = sf.stackImages(imageArray, 0.5)

        # cv2.imshow("Result", imgStacked)

        nid= userid[-1:]


        co = 0
        ro = 0
        grading = ""
        symb = []
        ns=1
        choos= "yABCD"
        for a in ans:
            if int(a) == myIndex[ro][co]:
                print(a)
                symb.append(f"{ns}. {choos[int(a)]}✅")
                grading += str(1)
            elif myIndex[ro][co] == 5:
                if ns<=9:
                    symb.append(f"{ns}.   ‼️ ")
                else:
                    symb.append(f"{ns}.  ‼️ ")
                grading += str(2)
            elif myIndex[ro][co] ==0:
                if ns <= 9:
                    symb.append(f"{ns}.   ❗️ ")
                else:
                    symb.append(f"{ns}.  ❗️ ")
                grading += str(0)
            else:
                print(a)
                symb.append(f"{ns}. {choos[myIndex[ro][co]]}❌")
                grading += str(0)
            ns+=1
            co += 1
            if (co == questions): ro += 1;co = 0
        firsts =  grading[:questions].count('1')
        seconds = grading[questions:questions*2].count('1')
        thirds = grading[questions*2:questions*3].count('1')
        if test_type =='90':
            resultg = (firsts * 1.1 + seconds * 3.1 + thirds * 2.1)
            resultg=round(resultg, 1)
            anw_message = f'{html.bold(html.quote(fullname))}\n———————————-\n<tg-spoiler>{resultg} ball</tg-spoiler>\n———————————-\n<tg-spoiler><b>Majburiy fanlar:</b> {firsts}\n<b>{second_s}:</b> {seconds}\n<b>{third_s}:</b> {thirds}</tg-spoiler>\n———————————-'
        else:
        
            resultg = (firsts + seconds + thirds )*1.0
            resultg=round(resultg, 1)
            anw_message = f'{html.bold(html.quote(fullname))}\n———————————-\n<tg-spoiler>{resultg} ta to‘g‘ri</tg-spoiler>\n———————————-'

        






        dsn_message = anw_message
        for i in range(questions):
            dsn_message+=f"\n{symb[i]}  {symb[i + questions]}  {symb[i + questions*2]}"

        await add_ans_message(int(id),teacher_id, dsn_message.replace('\n', '%^'), session_maker)



        await add_score(int(id),teacher_id, resultg, int(nid), test_type,session_maker)


        return anw_message




