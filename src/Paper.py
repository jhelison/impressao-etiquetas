from PIL import Image, ImageDraw, ImageFont
import math

from src.Tag import Tag

def cmToPixel(cms):
    return int(cms * 370.7952755906)

PAPERWIDHT = cmToPixel(21)
PAPERHEIGHT = cmToPixel(29.7)

class Paper():
    def __init__(self):
        self.paper = None
        
        self.buildPaper()
        
        
    def buildPaper(self):
        self.paper = Image.new('RGBA', (PAPERWIDHT, PAPERHEIGHT), 'white')
        
        tag = Tag("BOMBA SUBM. 220V 380W SD3/4 680 HB MASCOTE asd asd tesa", "220,0000", "000001")
        
        self.paper.paste(tag.img, (int((PAPERWIDHT / 2) - tag.TAGWIDHT / 2), int((PAPERHEIGHT / 2) - tag.TAGHEIGHT / 2)))
        
        self.paper.save('img.png')
        
        