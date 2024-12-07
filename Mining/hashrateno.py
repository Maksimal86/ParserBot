# -*- coding: utf-8 -*-
import time, re
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import requests, lxml
from bs4 import BeautifulSoup


class Browser():
    def __init__(self):
        self.options = Browser.set_options_selenium(self)
        self.s = Service(executable_path=r'C:/chromedriver.exe')
        self.driver = webdriver.Chrome(options=self.options, service=self.s)

    def set_options_selenium(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-blink-features")  # отключение функций блинк-рантайм
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--headless")  # скрытый запуск браузера
        options.add_argument('--no-sandobox')  # режим песочницы
        options.add_argument('--disable-gpu')  # во избежание ошибок
        options.add_argument('--disable-dev-shm-usage')  # для увеличения памяти для хрома
        options.add_argument('--lang=en')
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/106.0.0.0 YaBrowser/22.11.5.715 YaBrowser/2.5 Safari/537.36')
        prefs = {"profile.managed_default_content_settings.images": 2}  # не загружаем картинки
        options.add_experimental_option('prefs', prefs)  # не загружаем картинки
        return options

    def selenium_driver_close(self):
        self.driver.close()

    def selenium_driver_quit(self):
        self.driver.quit()

    def get_BeautifulSoup(self, card_name):
        url = f'https://www.hashrate.no/gpus/{card_name}'
        self.driver.get(url)
        page_source = self.driver.page_source.encode('cp1251', errors='ignore').decode('cp1251')
        with open('rplant.html', 'w') as file:
            file.write(page_source)
        soup = BeautifulSoup(page_source,'lxml')
        return soup

    def exclude_nice_hash(self):
        time.sleep(1)
        self.driver.find_element(By.XPATH,
                                 '/html/body/div/div[2]/div[5]/div[2]/div[2]/div[3]/div[2]/form[2]/div[3]/div[2]/div/'
                                 'input[1]').click()

    def get_main_tag(self):
        main_teg = self.get_BeautifulSoup('5700').find('ul', attrs={"id": "myUL"})
        return main_teg


    def get_list_of_names_coins(self):
        list_of_names_coins=[]
        web_element_of_names_coins = Browser.get_main_tag(self).find_all(class_='overlay')
        for i in web_element_of_names_coins:
            list_of_names_coins.append(re.search('\S*', i.text)[0])
        return list_of_names_coins


    def get_list_of_coins_profit(self):
        list_of_coins_profit = []
        web_element_coins_profit = Browser.get_main_tag(self).find_all(class_='w3-row inner')
        for i in web_element_coins_profit:
            teg = i.find_all(class_='w3-col l3 m3 s3 deviceData')[2].find('tr').find('td').text
            list_of_coins_profit.append(teg.strip(('$')))
        return list_of_coins_profit

    def get_dict_with_data(self):
        dict_with_data = {}
        for i, j in zip(self.get_list_of_names_coins(), self.get_list_of_coins_profit()):
            dict_with_data[i] = j
        return dict_with_data

    def get_sorting_dict(self):
        sorted_dict = sorted(self.get_dict_with_data().items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_dict)

    def converting_to_string_format(self, card):
        result = card + ' ' + str(self.get_sorting_dict())
        return result


def main_function():
    cards = ['1080','5600xt','5700']
    data_of_coins = Browser()
    for i in cards:
        data_of_coins.get_BeautifulSoup(i)
        data_of_coins.exclude_nice_hash()
        yield data_of_coins.converting_to_string_format(i)
    data_of_coins.selenium_driver_close()


if __name__ == '__main__':
    main_function()