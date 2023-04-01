import cv2
import numpy as np
import bot.test_scanner.scanner_f as sf
import io
from pyzbar.pyzbar import decode

from bot.db.user import get_st_answ


async def test_scanner_func(imgg, session_maker):
    ###################################
    # path = 'images/img_10.png'
    # img = cv2.imread(imgg)

    img = cv2.imdecode(np.frombuffer(imgg.read(), np.uint8), 1)

    code = decode(img)
    print(code)
    userid = int(code[0].data.decode('utf-8'))


    # Using cv2.rectangle() method
    # Draw a rectangle of black color of thickness -1 px

    # img = cv2.resize(img, (1000, 1000))
    h, w, c = img.shape


    if code[0].orientation == 'UP':
        pass
    elif code[0].orientation == 'LEFT':
        img= cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
    elif code[0].orientation == 'RIGHT':
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    elif code[0].orientation == 'DOWN':
        img = cv2.rotate(img, cv2.ROTATE_180)

    code = decode(img)

    start_x = code[0].polygon[3].x
    end_x = code[0].polygon[1].x
    end_y = code[0].polygon[1].y
    start_point = (start_x, 0)



    # Ending coordinate, here (125, 80)
    # represents the bottom right corner of rectangle
    end_point = (end_x, end_y)

    # Black color in BGR
    color = (255, 255, 255)

    # Line thickness of -1 px
    # Thickness of -1 will fill the entire shape
    thickness = -1
    img = cv2.rectangle(img, start_point, end_point, color, thickness)
    # cv2.imshow('dfs', img)


    imgWidth = 960
    imgHeight = 1280
    collums = 3
    questions = 30
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

        boxes = sf.splitBoxes(imgThresh)
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
        print("---------sfgsf-----",np.amax(myPixelVal))
        max_val = np.amax(myPixelVal) - 250.0
        if max_val>(np.amax(np.amin(np.amax(myPixelVal, axis = 2), axis=1))):
            pass
        else:
            max_val=1000.0


        for x in range(0, len(myPixelVal[0])):
            arr = myPixelVal[0][x]
            print("--------------",np.amax(arr))
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
            print("--------------", np.amax(arr)-10.0)
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
    ans = await get_st_answ(userid, session_maker)

    co = 0
    ro = 0
    grading=""
    for a in ans:
        if int(a) == myIndex[ro][co]:
            grading+=str(1)
        elif myIndex[ro][co] == 5:
            grading+=str(2)
        else:
            grading+=str(0)
        co += 1
        if (co == 30): ro += 1;co = 0

    resultg=(grading[:30].count('1')*1.1+grading[30:60].count('1')*3.1+grading[60:90].count('1')*2.1)


    cv2.waitKey(0)
    return grading, resultg
