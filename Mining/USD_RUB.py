# -*- coding: utf-8 -*-
import requests, lxml
from bs4 import BeautifulSoup


def get_page():
    return requests.get(get_url()).text.encode('cp1251',errors='replace').decode('cp1251')


def get_soup():
    return BeautifulSoup(get_page(), 'lxml')


def get_cource_usd_rub():
    for i in get_soup().select('main',class_='home-content'):
        return i.find(class_="col-md-2 col-xs-9 _dollar").next_sibling.next_sibling.text


def get_url():
    return 'https://cbr.ru/'


# def get_delta_cource():
#     return get_cource_usd_rub().text#next_sibling.next_sibling.text.strip().translate({ord(i):None for i in '()'}).replace(',','.')


def main():
    cource = str(get_cource_usd_rub())
    print(cource)
    return 'Курс ЦБ USD $ ' + cource.rstrip()[:-1] + 'руб.'


if __name__ == '__main__':
    main()