# -*- coding: utf-8 -*-
import datetime
import sys
import requests
import mytoken, HeshMh
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import mytoken
hashr=[]
hashlist = []
onlinehive=None
def options_add():

    options = webdriver.ChromeOptions()
    user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) + AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')
    options.add_argument('user-agent=%s' % user_agent)
    options.add_experimental_option("excludeSwitches", ['enable-automation'])  #  FOR uc
    options.add_argument("--disable-blink-features")  # отключение функций блинк-рантайм
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")  # скрытый запуск браузера
    options.add_argument('--no-sandobox')  # режим песочницы
    options.add_argument('--disable-gpu')  # во избежание ошибок
    options.add_argument('--disable-dev-shm-usage')  # увеличения памяти для хрома
    # options.add_argument('--disable-brouser-side-navigation')  # прекращение загрузки дополниетльных подресурсов при дляительной загрузки страницы
    options.add_argument('--lang=en')
    options.add_experimental_option('useAutomationExtension',
                                    False)  # опция отключает драйвер для установки других расширений Chrome, таких как CaptureScreenshot

    return options
def hive_cookies():
    mail_in = 'maksimal0484@yandex.ru'
    password='Dim2305Hive^'
    s = Service(executable_path=r'C:\yandexdriver.exe')  # расположение драйвера
    options = options_add()
    driver = webdriver.Chrome(service=s, options=options)
    url='https://ca1.hiveos.farm/login'
    driver.get(url)

    driver.find_element(By.XPATH,'//*[@id="app"]/div/div/div[1]/form/div[1]/input').send_keys(mail_in)
    driver.find_element(By.XPATH, '//*[@id="app"]/div/div/div[1]/form/div[2]/div[1]/input').send_keys(password)
    driver.find_element((By.XPATH,'//*[@id="app"]/div/div/div[1]/form/div[3]/input')).send_keys(google2fa)
    nfarm=mytoken.nfarms
    global hashr
    url=(f'https://the.hiveos.farm/api/v2/farms/{nfarm}')
    try:

        responce=requests.get(url, headers=mytoken.headers_hive)
        json=responce.json()['hashrates_by_coin']
        coin_hashrate=[]
        #coin=[]
        hashrate=[]
        j=0
        global onlinehive
        onlinehive =responce.json()['stats']['workers_online']
        for i in json:
            hshr = json[j]['hashrate']*1000
            coin=i['coin']
            j+=1
            hashrate.append(HeshMh.hashrate_coin(hshr, coin))
        print(str(hashrate).translate({ord(i): " " for i in ']['}))
        return str(hashrate).translate({ord(i): " " for i in ']['})
    except :
        with open('log.txt', 'a') as log:
            log.write(str('Hive' +str(datetime.datetime.now())) + str(sys.exc_info()) + '\n')
def save_onlinehive():
    hive_hashrate()
    print(onlinehive)
    return onlinehive
if __name__=='__main__':
    hive_hashrate()


# автоматическое получение печенья