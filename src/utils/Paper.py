from PIL import Image, ImageDraw, ImageFont
import math
import os

from src.utils.Tag import Tag

from src.config.ConfigDB import ConfigDB

def cmToPixel(cms):
    return int(cms * 370.7952755906)

PAPERWIDHT = cmToPixel(21)
PAPERHEIGHT = cmToPixel(29.7)

class Paper():
    def __init__(self):
        self.db = ConfigDB()
        self.paper = None
        
        self.PageHorizontalSpacing = cmToPixel(0.75)
        self.PageVerticalSpacing = cmToPixel(0.85)
        self.TagHorizontalSpacing = cmToPixel(0.25)
        self.TagVerticalSpacing = cmToPixel(0)
        
        self.maxHorizontalTags = 3
        self.maxVerticalTags = 9
                
    def buildPaper(self, data, startX, startY):
        images = []
        pagNum = 1
        
        xPos = startX
        yPos = startY
        
        self.paper = Image.new('RGB', (PAPERWIDHT, PAPERHEIGHT), 'white')
        
        tag = Tag("", "", "")
        
        HorizontalPos = self.PageHorizontalSpacing + (tag.TAGWIDHT + self.TagHorizontalSpacing) * (xPos - 1)
        VerticalPos = self.PageVerticalSpacing + (tag.TAGHEIGHT + self.TagVerticalSpacing) * (yPos - 1)
        
        for tagData in data:
            tag = Tag(tagData[1], tagData[2], tagData[0])
            
            tagNum = 1

            while tagNum <= tagData[3]:
                print(tagData[3], tagNum)
                self.paper.paste(tag.img, (HorizontalPos, VerticalPos))
                tagNum += 1
                xPos += 1
                
                HorizontalPos = HorizontalPos + tag.TAGWIDHT + self.TagHorizontalSpacing
                
                if xPos > self.maxHorizontalTags:
                    xPos = 1
                    yPos += 1
                    VerticalPos = VerticalPos + tag.TAGHEIGHT + self.TagVerticalSpacing
                    HorizontalPos = self.PageHorizontalSpacing
                    if yPos > self.maxVerticalTags:
                        pagNum += 1
                        yPos = 1
                        
                        images.append(self.paper)
                        self.paper = Image.new('RGB', (PAPERWIDHT, PAPERHEIGHT), 'white')
                        VerticalPos = self.PageVerticalSpacing
                        
        if xPos != 1 or yPos != 1:
            images.append(self.paper)
                
        outputLocation = self.db.get('leOutuput') + "\\out.pdf"
                
        images[0].save(outputLocation, save_all=True, append_images=images[1:], resolution=300)
        os.startfile(outputLocation)
                
                    
                    
                    # for y in range(self.maxVerticalTags):
                    #     for x in range(self.maxHorizontalTags):
                    #         self.paper.paste(tag.img, (HorizontalPos, VerticalPos))
                    #         HorizontalPos = HorizontalPos + tag.TAGWIDHT + self.TagHorizontalSpacing
                    #     HorizontalPos = self.PageHorizontalSpacing
                        
                
            
            

        
        