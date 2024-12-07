
import requests


def get_json():
    responce = requests.get('https://www.rbc.ru/crypto/v2/ajax/key-indicator-update/?_=1728673920742')
    return responce.json()


def get_cource():
    json = get_json()
    for i in range(19):
        name = json['shared_key_indicators_under_topline'][i]['item']['name']
        change = json['shared_key_indicators_under_topline'][i]['item']['change']
        closevalue = json['shared_key_indicators_under_topline'][i]['item']['closevalue']
        if name in ['BTC/USD','ETH/USD','XRP/USD','UST/USD']:
            yield name,  str(closevalue)+'$', str(round(change,2)) +'%'


if __name__ == '__main__':
    get_cource()