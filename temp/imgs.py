from bing_image_downloader import downloader
import logging
import time
import os

start = time.time()

logging.basicConfig(filename='strong_man.log', level=logging.DEBUG)

names_done = os.listdir('./images')


with open('strong_man.txt', encoding='utf-8') as file:
    strong_mans = file.read().split(',')
    
strong_mans = [(strong + " strongman") if "strongman" not in strong else strong for strong in strong_mans]
    
    
for index, query_string in enumerate(strong_mans):
    if query_string in names_done:
        continue

    try:
        now = time.time()
        timeToFinish = ((now - start) / (index + 1)) * (len(strong_mans) - (index + 1))
    
        print(f'   {query_string}, {index + 1}/{len(strong_mans)}   {(index + 1)/len(strong_mans) * 100}%   timeToF: {timeToFinish}s   '.center(100, '#'))
        
        downloader.download(query_string, limit=7,  output_dir='./images', adult_filter_off=True, force_replace=False)
    except:
        logging.error(f'{query_string} not downloded')
    
print(f'done'.center(100, '#'))
input()