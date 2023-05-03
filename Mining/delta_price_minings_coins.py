# -*- coding: utf-8 -*-
import sys, requests, lxml
from bs4 import BeautifulSoup

def hashrate_no_get_coin_price():
    return getting_coin_attrbutes()
def soup():
    url='https://www.hashrate.no/coins'
    responce = requests.get(url)
    soup = BeautifulSoup(responce.text, 'lxml')
    return soup
def getting_main_tag():
    list_main_teg = soup().findAll('div', class_='block deviceLink')
    return list_main_teg
def getting_coin_attrbutes():
    for i in getting_main_tag():
        coin_name=i.find('span',class_="deviceHeader").text
        coin_price=i.findAll('table')[1].find('td', class_ = 'coinsData').text
        coins_delta_price_hour =i.findAll('table')[1].findAll('td',class_='coinsInfo')[2].text
        coins_delta_price_day = i.findAll('table')[1].findAll('td', class_='coinsInfo')[4].text
        print(coin_name, coin_price, coins_delta_price_hour,coins_delta_price_day)
        yield coin_name, coin_price, coins_delta_price_hour+' за 1 час ',float(coins_delta_price_day[:-1])


if __name__ == '__main__':
    hashrate_no_get_coin_price()