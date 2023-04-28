# -*- coding: utf-8 -*-
import datetime, time
import sys, json, os
import requests
import mytoken, units_of_measurement
import sys
import time, datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import mytoken
def options_add():

    options = webdriver.ChromeOptions()
    user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) + AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')
    options.add_argument('user-agent=%s' % user_agent)
    options.add_experimental_option("excludeSwitches", ['enable-automation'])  #  FOR uc
    options.add_argument("--disable-blink-features")  # отключение функций блинк-рантайм
    options.add_argument("--disable-blink-features=AutomationControlled")
    #options.add_argument("--headless")  # скрытый запуск браузера
    options.add_argument('--no-sandobox')  # режим песочницы
    options.add_argument('--disable-gpu')  # во избежание ошибок
    options.add_argument('--disable-dev-shm-usage')  # увеличения памяти для хрома
    # options.add_argument('--disable-brouser-side-navigation')  # прекращение загрузки дополниетльных подресурсов при дляительной загрузки страницы
    options.add_argument('--lang=en')
    options.add_experimental_option('useAutomationExtension',
                                    False)  # опция отключает драйвер для установки других расширений Chrome, таких как CaptureScreenshot

    return options
hashr=[]
hashlist = []
onlinehive=None

def hive_hashrate():
    headers = mytoken.headers_hive
    print('run hive_hashrate')
    nfarm=mytoken.nfarms
    global hashr
    url=f'https://the.hiveos.farm/api/v2/farms/{nfarm}'
    try:
        with open('hive_cookie.txt','r') as file:
            cookies_from_file= json.load(file)
        necessary_cookies={}
        for cookie in cookies_from_file:
            dict_cookies={cookie["name"]:cookie["value"]}
            necessary_cookies.update(dict_cookies)
        responce =requests.get(url, headers=headers, cookies=necessary_cookies)
        print('json',responce.json())
        json_hashrate=responce.json()['hashrates_by_coin']
        hashrate=[]
        j=0
        global onlinehive
        json_rig_online =responce.json()['stats']['workers_online']
        for i in json_hashrate:
            rig_hashrate = json_hashrate[j]['hashrate']*1000
            name_coin=i['coin']
            j+=1
            hashrate.append(units_of_measurement.hashrate_coin(rig_hashrate, name_coin))
        with open('hive_work.txt', 'w') as file:
            file.write('True')
        print(str(hashrate).translate({ord(i): " " for i in ']['}))
        return str(hashrate).translate({ord(i): " " for i in ']['})
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('тип ошибки', exc_type, "модуль ",fname, 'строка' ,exc_tb.tb_lineno)

        with open('log.txt', 'a') as log:
            log.write(str('Hive' +str(datetime.datetime.now()) + str(sys.exc_info()) + '\n' + 'тип ошибки  '+ str(exc_type) + '  модуль  '+ str(fname) + '  строка  ' + str(exc_tb.tb_lineno)))
        with open('hive_work.txt','w') as file:
            file.write('False')
def hive_cookie(kod):
    print('run hive_cookie')
    s = Service(executable_path=r'C:\yandexdriver.exe')  # расположение драйвера
    #s = Service(executable_path=r'C:\chromedriver.exe')

    options = options_add()
    driver = webdriver.Chrome(service=s, options=options)

    url='https://the.hiveos.farm/'
    driver.get(url)
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(mytoken.loginhive, Keys.ENTER)
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(mytoken.passwordhive, Keys.ENTER)
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="kc-form-login"]/div[2]/div[2]/label/span').click()
    driver.find_element(By.XPATH, '//*[@id="kc-login"]/span').click()
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="kc-otp-login-form"]/div/label/span[2]/input[1]').send_keys(kod)
    time.sleep(7)
    cookie = driver.get_cookies()
    time.sleep(4)
    with open ('hive_cookie.txt', 'w') as file:
        json.dump(cookie, file)
    hive_hashrate()
    driver.close()
    driver.quit()
def hive_get_kod(kod):
    print('run hive_get_kod' )
    hive_cookie(kod)
    print('kod',kod)
def save_onlinehive():
    hive_hashrate()
    print(onlinehive)
    return onlinehive
if __name__=='__main__':
    hive_hashrate()


# автоматическое получение печенья