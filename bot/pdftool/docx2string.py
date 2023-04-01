from docxlatex import Document
import re
import random
def get_str(tid, file):
    doc = Document(file)
    print(type(doc))
    text = doc.get_text(image_dir=f'img/id{tid}', lltid=tid)
    return text
def get_string(text, test_type):
    print(text)

    r1 = re.findall(r'^#.+$', text, re.MULTILINE)
    r2 = re.findall(r"^[A-Z]\).+$|^\+[A-Z]\).+$", text, re.MULTILINE)

    if test_type == '90':
        l = [[], [], [], [], []]
        print(len(r1))
        print(len(r2))

        l[0] = [i for i in range(0, 10)]
        l[1] = [i for i in range(10, 20)]
        l[2] = [i for i in range(20, 30)]
        l[3] = [i for i in range(30, 60)]
        l[4] = [i for i in range(60, 90)]
        print(len(l[2]))
        ques = [[], [], []]
        chooses = [[], [], []]
        n = 0
        for i in range(90):
            if i == 30 or i == 60:
                n = n + 1
            ques[n].append(r1[i])
            chooses[n].append([])

        print(len(chooses[1]))
        n = 0
        m = 0
        v = 0
        for i in range(0, 360):
            if i == 120 or i == 240: n += 1; m = 0
            chooses[n][m].append(r2[i])
            v += 1
            if v == 4: m += 1;v = 0

        y = [0, 1, 2, 3]
        random.shuffle(l[0])
        random.shuffle(l[1])
        random.shuffle(l[2])
        random.shuffle(l[3])
        random.shuffle(l[4])
        # print(l)
        n = 0
        pattern = '^\+[A-Z]\).+$'
        chl = [" A)", " B)", " C)", " D)"]
        ans = ''
        text2 = ['', '', '']

        for i in l[0]:
            n += 1
            random.shuffle(y)

            ch = 0

            text2[
                0] += "<p class=\"dontsplit vs\" style=\"font-family: bitter; font-size: 14px; line-height: 17px; letter-spacing: 0.02em;\" >"

            print(r1[i].replace('#', str(n) + '.', 1))
            text2[0] += r1[i].replace('#', '<span style=" font-weight:500;">' + str(n) + '.</span>', 1)
            text2[0] += "</br>"
            for j in y:
                result = re.match(pattern, chooses[0][i][j])
                if result:
                    print(chl[ch], chooses[0][i][j][3:])
                    # text2 += '</br>'+chl[ch]+chooses[i][j][3:]
                    text2[0] += chl[ch] + chooses[0][i][j][3:]
                    ans+=str((ch + 1))
                else:
                    print(chl[ch], chooses[0][i][j][2:])
                    # text2 += '</br>'+chl[ch]+chooses[i][j][2:]
                    text2[0] += chl[ch] + chooses[0][i][j][2:]

                ch += 1
            print("\n")
            text2[0] += "</p>"
            text2[0] += "</br></br>"

        for i in l[1]:
            n += 1
            random.shuffle(y)

            ch = 0

            text2[
                0] += "<p class=\"dontsplit vs\" style=\"font-family: bitter; font-size: 14px; line-height: 17px; letter-spacing: 0.02em;\" >"

            print(r1[i].replace('#', str(n) + '.', 1))
            text2[0] += r1[i].replace('#', '<span style=" font-weight:500;">' + str(n) + '.</span>', 1)
            text2[0] += "</br>"
            for j in y:
                result = re.match(pattern, chooses[0][i][j])
                if result:
                    print(chl[ch], chooses[0][i][j][3:])
                    # text2 += '</br>'+chl[ch]+chooses[i][j][3:]
                    text2[0] += chl[ch] + chooses[0][i][j][3:]
                    ans+=str((ch + 1))
                else:
                    print(chl[ch], chooses[0][i][j][2:])
                    # text2 += '</br>'+chl[ch]+chooses[i][j][2:]
                    text2[0] += chl[ch] + chooses[0][i][j][2:]

                ch += 1
            print("\n")
            text2[0] += "</p>"
            text2[0] += "</br></br>"

        for i in l[2]:
            n += 1
            random.shuffle(y)

            ch = 0

            text2[
                0] += "<p class=\"dontsplit vs\" style=\"font-family: bitter; font-size: 14px; line-height: 17px; letter-spacing: 0.02em;\" >"

            print(r1[i].replace('#', str(n) + '.', 1))
            text2[0] += r1[i].replace('#', '<span style=" font-weight:500;">' + str(n) + '.</span>', 1)
            text2[0] += "</br>"
            for j in y:
                result = re.match(pattern, chooses[0][i][j])
                if result:
                    print(chl[ch], chooses[0][i][j][3:])
                    # text2 += '</br>'+chl[ch]+chooses[i][j][3:]
                    text2[0] += chl[ch] + chooses[0][i][j][3:]
                    ans+=str((ch + 1))
                else:
                    print(chl[ch], chooses[0][i][j][2:])
                    # text2 += '</br>'+chl[ch]+chooses[i][j][2:]
                    text2[0] += chl[ch] + chooses[0][i][j][2:]

                ch += 1
            print("\n")
            text2[0] += "</p>"
            text2[0] += "</br></br>"

        for i in l[3]:
            s = i - 30
            n += 1
            random.shuffle(y)

            ch = 0

            text2[
                1] += "<p class=\"dontsplit vs\" style=\"font-family: bitter; font-size: 14px; line-height: 17px; letter-spacing: 0.02em;\" >"

            print(r1[i].replace('#', str(n) + '.', 1))
            text2[1] += r1[i].replace('#', '<span style=" font-weight:500;">' + str(n) + '.</span>', 1)
            text2[1] += "</br>"
            for j in y:
                result = re.match(pattern, chooses[1][s][j])
                if result:
                    print(chl[ch], chooses[1][s][j][3:])
                    # text2 += '</br>'+chl[ch]+chooses[i][j][3:]
                    text2[1] += chl[ch] + chooses[1][s][j][3:]
                    ans+=str((ch + 1))
                else:
                    print(chl[ch], chooses[1][s][j][2:])
                    # text2 += '</br>'+chl[ch]+chooses[i][j][2:]
                    text2[1] += chl[ch] + chooses[1][s][j][2:]

                ch += 1
            print("\n")
            text2[1] += "</p>"
            text2[1] += "</br></br>"

        for i in l[4]:
            s = i - 60
            n += 1
            random.shuffle(y)

            ch = 0

            text2[
                2] += "<p class=\"dontsplit vs\" style=\"font-family: bitter; font-size: 14px; line-height: 17px; letter-spacing: 0.02em;\" >"

            print(r1[i].replace('#', str(n) + '.', 1))
            text2[2] += r1[i].replace('#', '<span style=" font-weight:500;">' + str(n) + '.</span>', 1)
            text2[2] += "</br>"
            for j in y:
                result = re.match(pattern, chooses[2][s][j])
                if result:
                    print(chl[ch], chooses[2][s][j][3:])
                    # text2 += '</br>'+chl[ch]+chooses[i][j][3:]
                    text2[2] += chl[ch] + chooses[2][s][j][3:]
                    ans+=str((ch + 1))
                else:
                    print(chl[ch], chooses[2][s][j][2:])
                    # text2 += '</br>'+chl[ch]+chooses[i][j][2:]
                    text2[2] += chl[ch] + chooses[2][s][j][2:]

                ch += 1
            print("\n")
            text2[2] += "</p>"
            text2[2] += "</br></br>"

        print(text2)

    else:
        l = [i for i in range(0, 30)]
        chooses = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [],
                   [], [], [], [], []]
        m = 0
        v = 0
        for i in range(0, 120):
            chooses[m].append(r2[i])
            v += 1
            if v == 4: m += 1;v = 0

        # print(r1)
        # print(chooses)
        # print(l)
        y = [0, 1, 2, 3]

        random.shuffle(l)
        # print(l)
        n = 0
        pattern = '^\+[A-Z]\).+$'
        chl = [" A)", " B)", " C)", " D)"]
        ans = ''
        text2 = ''
        for i in l:
            n += 1
            random.shuffle(y)

            ch = 0

            text2 += "<p class=\"dontsplit vs\" style=\"font-family: bitter; font-size: 14px; line-height: 17px; letter-spacing: 0.02em;\" >"

            print(r1[i].replace('#', str(n) + '.', 1))
            text2 += r1[i].replace('#', '<span style=" font-weight:500;">' + str(n) + '.</span>', 1)
            text2 += "</br>"
            for j in y:
                result = re.match(pattern, chooses[i][j])
                if result:
                    print(chl[ch], chooses[i][j][3:])
                    # text2 += '</br>'+chl[ch]+chooses[i][j][3:]
                    text2 += chl[ch] + chooses[i][j][3:]
                    ans+=str((ch + 1))
                else:
                    print(chl[ch], chooses[i][j][2:])
                    # text2 += '</br>'+chl[ch]+chooses[i][j][2:]
                    text2 += chl[ch] + chooses[i][j][2:]

                ch += 1
            print("\n")
            text2 += "</p>"
            text2 += "</br></br>"

    print(ans)
    return text2,ans



