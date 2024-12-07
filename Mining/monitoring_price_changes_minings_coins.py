# -*- coding: utf-8 -*-


import requests
import traceback
from bs4 import BeautifulSoup


def get_url():
    return 'https://www.hashrate.no/coins'


def get_soup():
    responce = requests.get(get_url())
    texthtmlpage = BeautifulSoup(responce.content, 'lxml')
    soup = BeautifulSoup(texthtmlpage.encode('cp1251', errors='replace').decode('cp1251'), 'lxml')
    return soup


def getting_main_tag():
    main_teg = get_soup().findAll('div', class_="w3-row")[9] # 9 - искомый div
    return main_teg


def get_all_blocks_of_coins():
    return getting_main_tag().find('ul', id='myUL').find_all('li')


def get_coin_name(i):
    return i.find('div',style="display: none;").text


def get_coin_price(i):
    return i.findAll('table')[0].findAll('td')[1].text


def get_coins_delta_price_hour(i):
    return i.findAll('tr')[1].find('td').text #за 1 час'


def get_coins_delta_price_day(i):
    return i.find('td', class_='infoChange').next_sibling.text


def getting_coin_attributes():
    try:
        j = 0
        for i in get_all_blocks_of_coins():
            j += 1
            try:
                yield get_coin_name(i), get_coin_price(i), get_coins_delta_price_hour(i), get_coins_delta_price_day(i)[:-1]
            except IndexError:
                continue
    except:
        traceback.print_exc()


if __name__ == '__main__':
    getting_coin_attributes()
