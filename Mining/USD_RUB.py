# -*- coding: utf-8 -*-
import requests, lxml
from bs4 import BeautifulSoup

def get_course():
    print('run get_course')
    url = 'https://quote.rbc.ru/ticker/59111'
    page=requests.get(url).text.encode('latin1', errors='ignore').decode('utf-8', errors='ignore')
    soup = BeautifulSoup(page, 'lxml')
    cource = soup.find('span', class_='chart__info__sum')
    delta_cource = cource.next_sibling.next_sibling.text.strip().translate({ord(i):None for i in '()'}).replace(',','.')
    return cource.text, delta_cource
if __name__ == '__main__':
    get_course()