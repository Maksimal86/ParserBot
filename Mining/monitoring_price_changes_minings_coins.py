# -*- coding: utf-8 -*-
import time

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
    main_teg = get_soup().find('ul') # 9 - искомый div
    return main_teg


def get_all_blocks_of_coins():
    return get_soup().find('ul', id='myUL').find_all('li')


def get_coin_name(i):
    print(i.find("div", class_="brand").text)
    return i.find("div", class_="brand").text


def get_coin_price(i):
    print(i.find("div", class_="estimates").text)
    return i.find("div", class_="estimates").text


def get_coins_delta_price(i):
    try:
        green = i.find("div", class_="green").text
        print(green)
        return green
    except AttributeError:
        orange = i.find("div", class_="orange").text
        print(orange)
        return orange



def getting_coin_attributes():
    for i in get_all_blocks_of_coins():
        try:
            print(get_coin_name(i), get_coin_price(i), get_coins_delta_price(i))
            yield get_coin_name(i), get_coin_price(i), get_coins_delta_price(i)
        except IndexError:
            continue


if __name__ == '__main__':
    getting_coin_attributes()
