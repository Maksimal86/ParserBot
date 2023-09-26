# -*- coding: utf-8 -*-
import lxml, sys
import requests
from bs4 import BeautifulSoup
import urls_for_cards
list_cards_url = [urls_for_cards.url_for_cards_1080, urls_for_cards.url_for_cards_5600,
                  urls_for_cards.url_for_cards_5700]


def get_response(url_of_card):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0 (Edition Yx 03)'}
    return requests.get(url_of_card, headers=headers)


def get_soup(text_of_response):
    return BeautifulSoup(text_of_response, "lxml")


def get_tag_with_name_of_coin(soup):
    tbody_tag = soup.tbody
    return tbody_tag.find_all('div', class_='ms-5 d-flex justify-content-between')


def get_name_of_card_for_result(url_for_cards):
    if url_for_cards == urls_for_cards.url_for_cards_1080:
        card = '1080'
        return card
    elif url_for_cards == urls_for_cards.url_for_cards_5700:
        card = '5700'
        return card
    elif url_for_cards == urls_for_cards.url_for_cards_5600:
        card = '5600'
        return card
    else:
        print(sys.exc_info())


def get_name_of_coin(tag):
    return tag.find('a').get_text()


def get_parent_tag(tag):
    return tag.find('a').find_parent('tr').find_all('td')


def get_incom(tag_strong):
    return tag_strong.find('strong').get_text()


def get_dict_of_coin_profit(tag, tag_strong):
    return {get_name_of_coin(tag).strip(): get_incom(tag_strong).strip()}


def get_profit_of_coins():
    number_of_coins_withdrawn = 5
    for url_of_card in list_cards_url:
        list_of_dictionaries_with_coins_profit = []
        response = get_response(url_of_card)
        soup = get_soup(response.text)
        for tag in get_tag_with_name_of_coin(soup):
            tag_line_number = 0
            if tag.find('a'):
                for tag_strong in get_parent_tag(tag):
                    tag_line_number += 1
                    if tag_line_number == 8:
                        list_of_dictionaries_with_coins_profit.append(str(get_dict_of_coin_profit(tag, tag_strong)))
                if len(list_of_dictionaries_with_coins_profit) == number_of_coins_withdrawn:
                    break
        yield get_name_of_card_for_result(url_of_card)+ str(list_of_dictionaries_with_coins_profit).translate(
            {ord(i): " " for i in '{}[]'})


if __name__ == '__main__':
    get_profit_of_coins()