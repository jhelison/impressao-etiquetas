import os
from PIL import Image, ImageDraw, ImageFont
import os
import math
import logging

logging.basicConfig(filename='strong_man.log', level=logging.DEBUG)

def getImgFromFolder(folder, file_name):

    def getImageInfo(name):
        data = {}
        
        data['name'] = name
        data['path'] = folder + '\\' + name
        
        img = Image.open(data['path'])
        data['size'] = img.size
        data['img'] = img
        
        return data

    def buildImage(imgs_data, rows):
        def calculateIndex(row, columns):
            begin_index = (row - 1) * columns
            if (row * columns) > len(imgs_data):
                end_index = len(imgs_data) - 1
            else:
                end_index = (row * columns) - 1

            return begin_index, end_index
            
        if rows > len(imgs_data):
            rows = len(imgs_data)
            
        x_pointer = 0
        y_pointer = 0
        columns = int(math.ceil(len(imgs_data) / rows))
        
        widths = []
        heights = []
        for i in range(1, rows + 1):
            begin_index, end_index = calculateIndex(i, columns)
                            
            widths.append(sum([data['size'][0] for data in imgs_data][begin_index:end_index + 1]))
            heights.append(max([data['size'][1] for data in imgs_data][begin_index:end_index + 1]))

        width = max([width for width in widths])
        height = sum([height for height in heights])
            
        new_img = Image.new('RGBA', (width, height), 'black')
        
        y_pointer = 0
        for i in range(rows):
            begin_index, end_index = calculateIndex(i + 1, columns)
            
            x_pointer = 0
            if i > 0:
                y_pointer += heights[i - 1
                                    ]
            for index, img_data in enumerate(imgs_data[begin_index:end_index + 1]):
                y_pointer = y_pointer
                new_img.paste(img_data['img'], (x_pointer, y_pointer))
                x_pointer = x_pointer + img_data['size'][0]
            
        return new_img

    def addWaterMark(img, text, sizePercent, padding):
        width, height = img.size
        
        new_height = int(height * (sizePercent + 1))
        
        new_img = Image.new('RGBA', (width, new_height), 'black')
        
        new_img.paste(img, (0,0))
        
        text_size = int((new_height - height - (padding * 2)) * 0.8)
        font = ImageFont.truetype("arial.ttf", size=text_size)
                
        idraw = ImageDraw.Draw(new_img)
        
        center_text = int(math.floor((width / 2) - (font.getsize(text)[0] / 2)))
        idraw.text((center_text , height), text, font=font)
        
        return new_img
        
    try:
        img_files = os.listdir(folder)[:-1]

        imgs_data = []    

        for f in img_files:
            if not f.endswith('.py'):
                imgs_data.append(getImageInfo(f))
            
        if file_name.endswith('strongman'):
            file_n = file_name[:-10]

        addWaterMark(buildImage(imgs_data, 2), file_n, 0.12, 10).save(f'./final_imgs/{file_n}.png')
        
    except Exception as e:
        logging.error(f'{file_n} error in turn into img with erro {e}')
        print('error ', file_n)
        



for p in os.listdir('./images'):
    print(p)
    f = os.getcwd() + '\\images' + '\\' + p
    getImgFromFolder(f, p)
    
input()