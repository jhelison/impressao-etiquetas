import requests
from bs4 import BeautifulSoup

with open('./html.html', encoding='utf-8') as file:
    html = file.read()
    
soup = BeautifulSoup(html, 'html.parser')

names = soup.findAll('span', {'class': 'listItem__title'})

names = [name.text for name in names]


