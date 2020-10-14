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
        
        self.PageHorizontalSpacing = cmToPixel(0.75)
        self.PageVerticalSpacing = cmToPixel(0.85)
        self.TagHorizontalSpacing = cmToPixel(0.25)
        self.TagVerticalSpacing = cmToPixel(0)
        
        self.maxHorizontalTags = 3
        self.maxVerticalTags = 9
        
        self.buildPaper()
        
    def buildPaper(self):
        self.paper = Image.new('RGB', (PAPERWIDHT, PAPERHEIGHT), 'white')
        
        tag = Tag("BOMBA SUBM. 220V 380W SD3/4 680 HB MASCOTE asd asd tesa", "220,0000", "000001")
        
        HorizontalPos = self.PageHorizontalSpacing
        VerticalPos = self.PageVerticalSpacing
        
        for y in range(self.maxVerticalTags):
            for x in range(self.maxHorizontalTags):
                self.paper.paste(tag.img, (HorizontalPos, VerticalPos))
                HorizontalPos = HorizontalPos + tag.TAGWIDHT + self.TagHorizontalSpacing
            HorizontalPos = self.PageHorizontalSpacing
            VerticalPos = VerticalPos + tag.TAGHEIGHT + self.TagVerticalSpacing
        
        
        
        self.paper.save('img.pdf')
        
        