# -*- coding: utf-8 -*-
import datetime
import sys
import requests
import time
import mytoken, HeshMh

period=180# время между опросами сервера
wdog1070=200 # минимальный хешрейт
wdog1060=90

def hashrate():

    global response
    url=('https://core-api.mineros.info/api/rigs/total-stat')
    '''организовать динамическое получение токена авторизации'''
    headers={'authority': 'core-api.mineros.info',
    'method': 'GET',
    'authorization': mytoken.tokenmineros,
    'farm': '15758',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0 (Edition Yx 03)'}
    hashrc=[] #список монет с хешрейтом
    try:

        for i in range(5):
            response = requests.get(url, headers=headers)
            print(response)
            if response.status_code <300:
                json = response.json()['hashrates']# распложение Нужных данных в Json формате
                j = 0

                for r in json:
                    coin = response.json()['hashrates'][j]['name'] # монета
                    hshr = (response.json()['hashrates'][j]['hashrate'])# хешрейт
                    HeshMh.hashrate_coin(hshr, coin)# записываем в нужных единицах измерения
                    j += 1
                    hashrc.append(HeshMh.hashrate_coin(hshr, coin))
                with open('log.txt', 'a') as log:

                    log.write('mineros  ' + str(datetime.datetime.now()) +' status code= ' +str(response.status_code))
                    log.write('\n')
                break
            else:
                with open('log.txt', 'a') as log:
                    log.write('mineros  ' + str(datetime.datetime.now()) + "Плохое соединение"+'\n')
                time.sleep(1)
        global onlineminer, rigsminer
        onlineminer = response.json()['online'] #количестов ригов онлайн
        rigsminer= str(response.json()['rigs']).translate({ord(i): " " for i in '][()'})# список онлайн и офлайн
        print(onlineminer, rigsminer, "mineros period= ",period)
        return str(hashrc).translate({ord(i): " " for i in '][()'}) #  убираем всё ненужное
    except IndexError:
        with open('log.txt', 'a', encoding='utf-8') as log:
            log.write('mineros '+str(datetime.datetime.now()) + ' нет соединения '+ str( sys.exc_info())+'\n')

def save_onlineminer():
    hashrate()
    return onlineminer
def save_rigsminer():
    return rigsminer

def reboot1070():
    url_comands=('https://core-api.mineros.info/api/commands')
    payload={'cmd': "shutdown -r now", 'tokens': ["bpgZwXxaao9kCDqRBooKV6b8NdNT1S5p"]}
    headers={'authority': 'core-api.mineros.info',
        'method': 'POST',
        'authorization': mytoken.tokenmineros,
        'farm': '15758',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0 (Edition Yx 03)'}
    response = requests.post(url_comands, headers=headers, json=payload)
    #print(response.status_code, response)
    with open('log.txt', 'a') as log:
        log.write('reboot1070'+ str(datetime.datetime.now()) + 'status code=  ' + str(response.status_code))


def reboot1060():
    url_comands=('https://core-api.mineros.info/api/commands')
    payload={'cmd': "shutdown -r now", 'tokens': ["AuyD2kofcNULHLLnVtRS9ZsXbqMViSyh"]}
    headers={'authority': 'core-api.mineros.info',
        'method': 'POST',
        'authorization': mytoken.tokenmineros,
        'farm': '15758',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 OPR/93.0.0.0 (Edition Yx 03)'}
    response = requests.post(url_comands, headers=headers, json=payload)
    print(response.status_code, response)
    with open('log.txt', 'a') as log:
        log.write('reboot1060' + str(datetime.datetime.now()) + 'status code=  ' + str(response.status_code))


if __name__ == '__main__':
    hashrate()
# проработать работу wdog с предупреждениями.
 # избавиться от большого количества вызова функций
 #wdog на все монеты
# проработать возможность отслеживания хешрейта из  mineros и передачей сообщения в request