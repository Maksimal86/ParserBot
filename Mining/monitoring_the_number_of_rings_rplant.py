# -*- coding: utf-8 -*-
import time, datetime
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from requests.exceptions import ConnectionError
from Selenium_Driver import get_driver_selenium


def get_rplant_url():
    return 'https://pool.rplant.xyz/#clore'


def get_wallet():
    return 'AchPZxKXt1fL9G9kbyX3TVFjhnPRmHZF5Q'


def get_right_page(driver):
    print('run right page')
    driver.get(get_rplant_url())


def find_wallet(driver):
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR,'#getMiner0').send_keys(get_wallet())
    driver.find_element(By.CSS_SELECTOR,'.uk-form-icon.uk-form-small.uk-form-icon-flip.uk-icon').click()


def quantity_of_miners(driver):
    time.sleep(5)
    return driver.find_element(By.CSS_SELECTOR, '#workersCount2').text


def mgn_hashrate(driver):
    time.sleep(5)
    return driver.find_element(By.CSS_SELECTOR,'#statsMinerHr').text


def sr_hashrate(driver):
    time.sleep(5)
    return driver.find_element(By.CSS_SELECTOR, '#statsMinerAvgHr').text


def get_table_with_names_and_hashrate(driver):
    time.sleep(5)
    return driver.find_element(By.CSS_SELECTOR, '#boxesWorkers').find_element\
        (By.CSS_SELECTOR, 'tbody').find_elements(By.CSS_SELECTOR, 'tr')


def hashrate_of_rigs(driver):
    time.sleep(4)
    result = ''
    table = get_table_with_names_and_hashrate(driver)
    for i in table:
        names_of_rig = i.find_element(By.CSS_SELECTOR, 'td').text
        hashrate = i.find_element(By.CSS_SELECTOR, "[id^='statsHashrate']").text
        name_and_hashrate = names_of_rig + ' ' + hashrate + '\n'
        result += name_and_hashrate
    return result


def monitoring_of_mining():
    print('monitoring_of_mining()')
    driver = get_driver_selenium()
    driver.get(get_rplant_url())
    find_wallet(driver)
    hashrate_of_rigs(driver)
    return int(quantity_of_miners(driver)), mgn_hashrate(driver), sr_hashrate(driver), hashrate_of_rigs(driver)


if __name__ == '__main__':
    monitoring_of_mining()

# def get_headers():
#     return mytoken.headers_hive


# def get_responce():
#     cookies = get_necessary_cookies()
#     if cookies == False:
#         return False
#     return requests.get(get_rplant_url(), headers=get_headers(), cookies = cookies)


# def get_necessary_cookies():
#     necessary_cookies = {}
#     try:
#         with open('hive_cookie.txt', 'r') as file:
#             cookies_from_file = json.load(file)
#         for cookie in cookies_from_file:
#             dict_cookies = {cookie["name"]: cookie["value"]}
#             necessary_cookies.update(dict_cookies)
#         return necessary_cookies
#     except:
#         return False


# def get_quantity_of_rig_online():
#     if get_responce() == False:
#         return False
#     try:
#         return get_responce().json()['stats']['workers_online']
#     except KeyError:
#         return False

# Service(executable_path=r'C:\chromedriver.exe')


# def get_cookies(driver):
#     return driver.get_cookies()


# def save_cookies(driver):
#     with open ('hive_cookie.txt', 'w') as file:
#         json.dump(get_cookies(driver), file)




