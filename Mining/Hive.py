# -*- coding: utf-8 -*-
import sys, os, inspect
import requests
import mytoken, units_of_measurement
import time, datetime
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
from requests.exceptions import ConnectionError
from Selenium_Driver import get_driver_selenium_edge


def get_farms_api_url():
    return f'https://the.hiveos.farm/api/v2/farms/{get_id_farm()}'


def get_id_farm():
    return mytoken.id_farms


def get_headers():
    return mytoken.headers_hive


def get_responce():
    cookies = get_necessary_cookies()
    if cookies == False:
        return False
    return requests.get(get_farms_api_url(), headers=get_headers(), cookies = cookies)


def get_necessary_cookies():
    necessary_cookies = {}
    try:
        with open('hive_cookie.txt', 'r') as file:
            cookies_from_file = json.load(file)
        for cookie in cookies_from_file:
            dict_cookies = {cookie["name"]: cookie["value"]}
            necessary_cookies.update(dict_cookies)
        return necessary_cookies
    except:
        return False


def get_quantity_of_rig_online():
    if get_responce() == False:
        return False
    try:
        return get_responce().json()['stats']['workers_online']
    except KeyError:
        return False


def get_farms_url():
    return 'https://the.hiveos.farm/'


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
    time.sleep(2)
    ''' remember me'''
    driver.find_element(By.XPATH, '//*[@id="kc-form-login"]/div[2]/div[2]/label/span').click()
    time.sleep(2)
    ''' нажимаем на вход'''
    driver.find_element(By.XPATH, '//*[@id="kc-login"]/span').click()
    time.sleep(2)


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


def enter_kod(driver, kod):
    driver.find_element(By.XPATH, '//*[@id="kc-otp-login-form"]/div/span/input[1]').send_keys(kod)


def check_need_enter_kod(driver):
    try:
        driver.find_element(By.XPATH, '//*[@id="kc-otp-login-form"]/div/span/input[1]')
        # Для получения кода аутентификатора
        with open('hive_work.txt', 'w') as file:
            file.write('False')
    except NoSuchElementException:
        pass


def get_hive_cookie(kod='нет кода'):
    print('run hive_cookie')
    driver = get_driver_selenium()
    get_right_page(driver)
    log_in_hive(driver)
    time.sleep(2)
    enter_kod(driver, kod)
    time.sleep(2)
    save_cookies(driver)
    driver.close()
    driver.quit()
    get_hive_hashrate()


def hive_get_kod_of_authenticator(kod):
    print('run hive_get_kod')
    get_hive_cookie(kod)
    print('kod',kod)


def get_hive_hashrate():
    print('run hive_hashrate ЗАПУЩЕН',inspect.stack()[1][3])
    try:
        quantity_of_rig_online = get_quantity_of_rig_online()
        if quantity_of_rig_online == False:
            return False
        else:
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

if __name__=='__main__':
    get_hive_hashrate()


# код получается, но не вводится