
import requests


def get_json():
    responce = requests.get('https://www.rbc.ru/crypto/v2/ajax/key-indicator-update/?_=1728673920742')
    return responce.json()


def get_cource():
    json = get_json()
    list_result = []
    try:
        for i in range(20):
            name = json['shared_key_indicators_under_topline'][i]['item']['name']
            change = json['shared_key_indicators_under_topline'][i]['item']['change']
            closevalue = json['shared_key_indicators_under_topline'][i]['item']['closevalue']
            if name in ['BTC/USD','ETH/USD','XRP/USD','UST/USD']:
                list_result.append(name +' ' + str(closevalue) + '$' + ' ' + str(round(change,2)) +'%')
    except IndexError:
        print(list_result)
        return list_result


if __name__ == '__main__':
    get_cource()