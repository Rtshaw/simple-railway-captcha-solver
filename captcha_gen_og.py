from PIL import Image, ImageDraw, ImageFont
from random import randint
import csv
import numpy as np
FONTPATH = ["./data/font/times-bold.ttf"]
ENGSTR = "ABCDEFGHJKLMNPRSTUVWXYZabcdefghjklmnprstuvwxyz" # 沒有 1 i I q Q O o
LETTERSTR = "23456789ABCDEFGHJKLMNPRSTUVWXYZabcdefghjklmnprstuvwxyz"

# 字符
class captchatext:
    def __init__(self, priority, offset, captchalen, engletter, ENGNOLIMIT):
        self.engletter = engletter
        if ENGNOLIMIT:
            engletter = True if randint(1, len(ENGSTR)) >= 9 else False
        if engletter:
            self.letter = ENGSTR[randint(0, len(ENGSTR) - 1)]
        else:
            self.letter = str(randint(2, 9))

        self.color = [0, 0, 0] # 文字顏色
        self.priority = priority
        self.offset = offset
        self.next_offset = 0
        self.captchalen = captchalen



    def draw(self, image, letter, angle):

        color = (self.color[0], self.color[1], self.color[2], 255)
        font = ImageFont.truetype(FONTPATH[0], randint(25, 25) * 10) # 字型
        text = Image.new("RGBA", (font.getsize(letter)[0], 300), (0, 0, 0, 0))
        textdraw = ImageDraw.Draw(text)
        textdraw.text((0, 0), letter, font=font, fill=color)
        text = text.rotate(angle, expand=True)
        text = text.resize((int(text.size[0] / 10), int(text.size[1] / 10)))
        base = int(self.priority * (140 / self.captchalen))
        rand_min = (self.offset - base - 4) if (self.offset - base - 4) >= -15 else -15
        rand_min = 0 if self.priority == 0 else rand_min
        # rand_min = randint(-50, -15)
        avg_dp = int(157 / self.captchalen)
        rand_max = (avg_dp - text.size[0]) if self.priority == self.captchalen - 1 else (avg_dp - text.size[0] + 20)
        try:
            displace = randint(rand_min, rand_max)
        except:
            displace = rand_max

        displace = randint(-125, -25)
        print(displace)
        location = (base + displace, randint(3, 10))
        self.next_offset = location[0] + text.size[0]
        image.paste(text, location, text)

        


def generate(GENNUM, SAVEPATH, ENGP=25, FIVEP=0, ENGNOLIMIT=False, filename="train"):
    captchacsv = open(SAVEPATH + "captcha_{:s}.csv".format(filename), 'w', encoding = 'utf8', newline = '')
    lencsv = open(SAVEPATH + "len_{:s}.csv".format(filename), 'w', encoding = 'utf8', newline = '')
    letterlist = []
    lenlist = []
    for index in range(1, GENNUM + 1, 1):
        captchastr = ""
        captchalen = 5
        engat = randint(0, captchalen - 1) if randint(1, 100) <= ENGP else -1
        bgcolor = [randint(250, 250) for _ in range(3)] # 圖片背景顏色
        captcha = Image.new('RGBA', (157, 41), (bgcolor[0], bgcolor[1], bgcolor[2], 255)) # 底圖
        offset = 0

        # captcha.show()

        angle = [randint(-15, -5), randint(5, 15)]

        for i in range(captchalen):
            newtext = captchatext(i, offset, captchalen, (True if engat == i else False), ENGNOLIMIT)
            offset = newtext.next_offset
            captchastr += str(newtext.letter)
        
        
        newtext.draw(image=captcha, letter=captchastr, angle=angle[randint(0, 1)])
        letterlist.append([str(index).zfill(len(str(GENNUM))), captchastr])
        lenlist.append([str(index).zfill(len(str(GENNUM))), captchalen])

        captcha.convert("RGB").save(SAVEPATH + str(index).zfill(len(str(GENNUM))) + ".png", "PNG")

    writer = csv.writer(captchacsv)
    writer.writerows(letterlist)
    writer = csv.writer(lencsv)
    writer.writerows(lenlist)
    captchacsv.close()
    lencsv.close()


if __name__ == "__main__":
    generate(50000, "./data/5_imitate_train_set/",  ENGP=100, FIVEP=100, ENGNOLIMIT=True, filename="train")
    generate(10240, "./data/5_imitate_vali_set/",  ENGP=100, FIVEP=100, ENGNOLIMIT=True, filename="vali")
