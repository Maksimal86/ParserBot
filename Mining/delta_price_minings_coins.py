# -*- coding: utf-8 -*-
import requests, json
from bs4 import BeautifulSoup
import lxml
import time, datetime, sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
error = 1  # флаг ответа сайта ???? проверить
def options_add():
    options = webdriver.ChromeOptions()
    # options = undetected_chromedriver.ChromeOptions()
    # options.page_load_strategy = 'eager'#WebDriver ожидает, пока не будет возвращен запуск события DOMContentLoaded.
    # options.add_argument("set_window_size(0, 0)")
    options.add_experimental_option("excludeSwitches", ['enable-automation'])
    options.add_argument("--disable-blink-features")  # отключение функций блинк-рантайм
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")  # скрытый запуск браузера
    options.add_argument('--no-sandobox')  # режим песочницы
    options.add_argument('--disable-gpu')  # во избежание ошибок
    options.add_argument('--disable-dev-shm-usage')  # для увеличеня памяти для хрома
    # options.add_argument('--disable-brouser-side-navigation')  # прекращение загрузки дополниетльных подресурсов при дляительной загрузки страницы
    options.add_argument('--lang=en')
    options.add_experimental_option('useAutomationExtension',
                                    False)  # опция отключает драйвер для установки других расширений Chrome, таких как CaptureScreenshot
    # options.add_argument(
    #   '--start-maximized')  # Запускает браузер в развернутом виде, независимо от любых предыдущих настроек.
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.5.715 Yowser/2.5 Safari/537.36')  # меняем заголовок запроса
    prefs = {"profile.managed_default_content_settings.images": 2}  # не загружаем картинки
    # options.add_experimental_option('prefs', prefs)  # не загружаем картинки
    return options


def hashrate_no_get_coin_price():
    url='https://www.hashrate.no/coins'
    s = Service(executable_path=r'C:\yandexdriver.exe')  # расположение драйвера
    options = options_add()
    driver = webdriver.Chrome(service=s, options=options)
    driver.get(url)
    try:
        for i in range(1,50):
            try:
                coin_name=driver.find_element(By.XPATH, f'/html/body/div/div[2]/div[2]/div[3]/div[2]/div[{i}]/a/div/div[1]/div/span').text
            except NoSuchElementException:
                continue
            price_coin=driver.find_element(By.XPATH,f'/html/body/div/div[2]/div[2]/div[3]/div[2]/div[{i}]/a/div/div[2]/div/table/tbody/tr[1]/td').text
            delta_price_day=driver.find_element(By.XPATH, f'/html/body/div/div[2]/div[2]/div[3]/div[2]/div[{i}]/a/div/div[2]/div/table/tbody/tr[4]/td[2]').text
            print(coin_name, price_coin, delta_price_day)
            yield coin_name, price_coin, float(delta_price_day[:-1])
    except:
        print( sys.exc_info())
    finally:
        driver.close()
        driver.quit()

if __name__ == '__main__':
    hashrate_no_get_coin_price()