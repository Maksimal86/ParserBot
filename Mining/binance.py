# -*- coding: utf-8 -*-
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


def set_options_of_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/106.0.0.0 YaBrowser/22.11.5.715 Yowser/2.5 Safari/537.36')
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option('prefs', prefs)
    return options


def get_service_selenium():
    return Service(executable_path=r'C:\yandexdriver.exe')


def get_driver_selenium():
    options = set_options_of_selenium()
    service = get_service_selenium()
    return webdriver.Chrome(service=service, options=options)


def get_url(page):
    return f'https://www.binance.com/en/markets/overview?p={page}'


def get_coin(driver,i):
    return driver.find_element(By.XPATH, f'//*[@id="tabContainer"]/div[2]/div[3]/div/div/div[2]/div[{i}]/div/a/div/div/div[2]/div').text


def get_price_of_coin(driver, i):
    return driver.find_element(By.XPATH, f'//*[@id="tabContainer"]/div[2]/div[3]/div/div/div[2]/div[{i}]/div/div[1]').text


def get_delta_of_coin_price(driver, i):
    return driver.find_element(By.XPATH, f'//*[@id="tabContainer"]/div[2]/div[3]/div/div/div[2]/div[{i}]/div/div[2]').text


def get_cource_from_binance():
    driver = get_driver_selenium()
    data_of_coin = []
    for page in [1,2,3]:
        driver.get(get_url(page))
        time.sleep(1)
        find_coin=['BTC', 'ETH','XRP','FIL','SKL','ETHW','USDT']
        for i in range(1,16):
            coin = get_coin(driver,i)
            price_of_coin = get_price_of_coin(driver,i)
            delta_of_coin_price = get_delta_of_coin_price(driver, i)
            if coin in find_coin:
                data_of_coin.append(coin + ' ' + price_of_coin + ' ' + delta_of_coin_price)
                print(coin + ' ' + price_of_coin + ' ' + delta_of_coin_price)
            yield coin, price_of_coin, delta_of_coin_price
    driver.close()
    driver.quit()


if __name__ == '__main__':
    get_cource_from_binance()