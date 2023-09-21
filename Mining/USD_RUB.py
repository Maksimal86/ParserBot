# -*- coding: utf-8 -*-
import requests, lxml
from bs4 import BeautifulSoup


def get_page():
    return requests.get(get_url()).text.encode('latin1', errors='ignore').decode('utf-8', errors='ignore')


def get_soup():
    return BeautifulSoup(get_page(), 'lxml')


def get_cource_usd_rub():
    return get_soup().find('span', class_='chart__info__sum')


def get_url():
    return 'https://quote.rbc.ru/ticker/59111'


def get_delta_cource():
    return get_cource_usd_rub().next_sibling.next_sibling.text.strip().translate({ord(i):None for i in '()'}).replace(',','.')


def main():
    cource = get_cource_usd_rub()
    delta_cource = get_delta_cource()
    print(cource.text, delta_cource)
    return cource.text, delta_cource
if __name__ == '__main__':
    main()