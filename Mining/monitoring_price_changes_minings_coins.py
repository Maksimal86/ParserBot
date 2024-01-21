# -*- coding: utf-8 -*-


import sys, requests, lxml
from bs4 import BeautifulSoup


def hashrateno_get_coin_price():
    return getting_coin_attrbutes()


def get_url():
    return 'https://www.hashrate.no/coins'


def get_soup():
    responce = requests.get(get_url())
    soup = BeautifulSoup(responce.text, 'lxml')
    return soup


def getting_main_tag():
    list_main_teg = get_soup().findAll('div', class_='block deviceLink')
    return list_main_teg


def get_coin_name(i):
    return i.find('span',class_="deviceHeader").text


def get_coin_price(i):
    return i.findAll('table')[1].find('td', class_='coinsData').text


def get_coins_delta_price_hour(i):
    return i.findAll('table')[1].findAll('td', class_='coinsInfo')[1].text+ ' за 1 час'


def get_coins_delta_price_day(i):
    return i.findAll('table')[1].findAll('td', class_='coinsInfo')[3].text


def getting_coin_attrbutes():
    for i in getting_main_tag():
        yield get_coin_name(i), get_coin_price(i), get_coins_delta_price_hour(i), get_coins_delta_price_day(i)[:-1]


if __name__ == '__main__':
    hashrateno_get_coin_price()