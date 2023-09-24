# -*- coding: utf-8 -*-
import sys, os, inspect
import requests
import mytoken, units_of_measurement
import time, datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
from requests.exceptions import ConnectionError


def set_options_of_selenium():
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
    options.add_experimental_option('useAutomationExtension', False)
    return options


def get_farms_api_url():
    return f'https://the.hiveos.farm/api/v2/farms/{get_id_farm()}'


def get_id_farm():
    return mytoken.id_farms


def get_headers():
    return mytoken.headers_hive


def get_responce():
    return requests.get(get_farms_api_url(), headers=get_headers(), cookies=get_necessary_cookies())


def get_necessary_cookies():
    necessary_cookies = {}
    with open('hive_cookie.txt', 'r') as file:
        cookies_from_file = json.load(file)
    for cookie in cookies_from_file:
        dict_cookies = {cookie["name"]: cookie["value"]}
        necessary_cookies.update(dict_cookies)
    return necessary_cookies


def get_quantity_of_rig_online():
    return get_responce().json()['stats']['workers_online']


def get_farms_url():
    return 'https://the.hiveos.farm/'


def get_service_selenium():
    return Service(executable_path=r'C:\yandexdriver.exe')
# Service(executable_path=r'C:\chromedriver.exe')


def get_driver_selenium():
    options = set_options_of_selenium()
    service = get_service_selenium()
    return webdriver.Chrome(service=service, options=options)


def get_right_page(driver):
    print('run right page')
    driver.get(get_farms_url())


def get_cookies(driver):
    return driver.get_cookies()


def save_cookies(driver):
    with open ('hive_cookie.txt', 'w') as file:
        json.dump(get_cookies(driver), file)


def log_in_hive(driver):
    driver.find_element(By.XPATH, '//*[@id="username"]').send_keys(mytoken.loginhive, Keys.ENTER)
    time.sleep(2)
    driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(mytoken.passwordhive, Keys.ENTER)
    time.sleep(3)
    driver.find_element(By.XPATH, '//*[@id="kc-form-login"]/div[2]/div[2]/label/span').click()
    driver.find_element(By.XPATH, '//*[@id="kc-login"]/span').click()


def get_hashrates_of_all_coins():
    hashrates = get_responce().json()['hashrates_by_coin']
    print('hashrates', hashrates)
    list_of_hashrates_of_different_coins = []
    number_of_coins_mined = 0 # переназвать
    for i in hashrates:
        print('i =', i)
        rigs_hashrate = hashrates[number_of_coins_mined]['hashrate'] * 1000
        name_coin = i['coin']
        number_of_coins_mined += 1
        list_of_hashrates_of_different_coins.append(units_of_measurement.main(rigs_hashrate, name_coin))
    return list_of_hashrates_of_different_coins


def get_hive_hashrate():
    print('run hive_hashrate')
    try:
        quantity_of_rig_online = get_quantity_of_rig_online()
        # Для получения кода аутентификатора
        with open('hive_work.txt', 'w') as file:
            file.write('True')
        print('quantity_of_rig_online', quantity_of_rig_online)
        print(str(get_hashrates_of_all_coins()).translate({ord(i): " " for i in ']['}))
        return str(get_hashrates_of_all_coins()).translate({ord(i): " " for i in ']['})
    except ConnectionError or KeyError:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print('тип ошибки', exc_type, "модуль ",file_name, 'строка' ,exc_tb.tb_lineno)
        with open('log.txt', 'a') as log:
            log.write(str('Hive' + str(datetime.datetime.now()) + str(sys.exc_info()) + '\n' + 'тип ошибки  ' + str(
                exc_type) + '  модуль  ' + str(file_name) + '  строка  ' + str(exc_tb.tb_lineno)))
        get_hive_cookie()
        # Для получения кода аутентификатора
        with open('hive_work.txt', 'w') as file:
            file.write('False')


def enter_kod(driver, kod):
    driver.find_element(By.XPATH, '//*[@id="kc-otp-login-form"]/div/span/input[1]').send_keys(kod)


def get_hive_cookie(kod='нет кода'):
    print('run hive_cookie')
    driver = get_driver_selenium()
    get_right_page(driver)
    log_in_hive(driver)
    if inspect.stack()[1][3]  ==  'hive_get_kod_of_authenticator':
        enter_kod(driver, kod)
    time.sleep(3)
    save_cookies(driver)
    driver.close()
    driver.quit()
    get_hive_hashrate()


def hive_get_kod_of_authenticator(kod):
    print('run hive_get_kod')
    get_hive_cookie(kod)
    print('kod',kod)

if __name__=='__main__':
    get_hive_hashrate()


