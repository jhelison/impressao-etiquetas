from PIL import Image, ImageDraw, ImageFont
import math

def cmToPixel(cms):
    return int(cms * 370.7952755906)


class Tag():    
    def __init__(self, name, value, code):
        self.TAGWIDHT = cmToPixel(6.35)
        self.TAGHEIGHT = cmToPixel(3.1)
        
        self.img = None
        
        self.name = name
        self.value = value
        self.code = code
        
        self.buildImg()
        self.addLogoText()
        self.addProductText()
        self.addValue()
        self.addCode()
        
    def buildImg(self):
        self.img = Image.new('RGBA', (self.TAGWIDHT, self.TAGHEIGHT), 'white')
        self.idraw = ImageDraw.Draw(self.img)
        
    def addLogoText(self):
        font = ImageFont.truetype("arialbi.ttf", size=150)
        center_text = int(math.floor((self.TAGWIDHT / 2) - (font.getsize("O TIJOLÂO")[0] / 2)))
        self.idraw.text((center_text, 60), "O TIJOLÂO", 'black', font)
        
    def addProductText(self):
        lines = []
        words = (self.name).split()
        line = ''
        for index, word in enumerate(words):
            nextWord = False
            while not nextWord:
                if len(line + ' ' + word) <= 22:
                    if line == '':
                        line = word
                    else:
                        line = line + ' ' + word
                    nextWord = True
                    if index == len(words) - 1:
                        lines.append(line)
                else:
                    lines.append(line)
                    line = ''

        print(lines)

        font = ImageFont.truetype("arial.ttf", size=180)
        
        for index, line in enumerate(lines):
            if len(lines) == 1:
                startinPoint = (180 * 3) / 2 - (180 / 2)
            if len(lines) == 2:
                startinPoint = ((180 * 3) / 2) - 180
            if len(lines) == 3:
                startinPoint = 0
                
            heightPosition = 60 + 150 + 30 + startinPoint + 180 * index
            center_text = int(math.floor((self.TAGWIDHT / 2) - (font.getsize(line)[0] / 2)))
            self.idraw.text((center_text, heightPosition), line, 'black', font)
            
    def addValue(self):
        text = self.value
        font = ImageFont.truetype("arial.ttf", size=300)
        center_text = int(math.floor((self.TAGWIDHT / 2) - (font.getsize(text)[0] / 2)))
        heightPosition = 60 + 150 + 180 * 3 + 60 - 65
        self.idraw.text((center_text, heightPosition), text, 'black', font)
        
    def addCode(self):
        text = "REF:" + self.code
        
        font = ImageFont.truetype("arial.ttf", size=80)
        center_text = int(math.floor((self.TAGWIDHT / 2) - (font.getsize(text)[0] / 2)))
        heightPosition = 60 + 150 + 180 * 3 + 60 + 240 + 5
        
        self.idraw.text((center_text, heightPosition), text, 'black', font)
        
    