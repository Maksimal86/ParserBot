# -*- coding: utf-8 -*-
import time, datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


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
            'Chrome/106.0.0.0 YaBrowser/22.11.5.715 Yowser/2.5 Safari/537.36')
        prefs = {"profile.managed_default_content_settings.images": 2}  # не загружаем картинки
        options.add_experimental_option('prefs', prefs)  # не загружаем картинки
        return options

    def start_selenium_browser(self):
        self.options = Browser.set_options_selenium(self)
        self.driver = webdriver.Chrome(options=self.options, service=self.s)

    def selenium_driver_close(self):
        self.driver.close()

    def selenium_driver_quit(self):
        self.driver.quit()

    def get_driver_url(self, card_name):
        url = f'https://www.hashrate.no/gpus/{card_name}'
        self.driver.get(url)

    def exclude_nice_hash(self):
        time.sleep(1)
        self.driver.find_element(By.XPATH,
                                 '/html/body/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[2]/form[2]/div[3]/div[2]/div/input[2]').click()



    def get_main_teg(self):
        main_teg = self.driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[3]')
        return main_teg

    def get_list_of_names_coins(self):
        list_of_names_coins = []
        web_element_coins_names = Browser.get_main_teg(self).find_elements(By.CLASS_NAME, 'deviceHeader')
        for i in web_element_coins_names:
            list_of_names_coins.append(i)
        return list_of_names_coins

    def get_list_of_coins_profit(self):
        list_of_coins_profit = []
        web_element_coins_profit = Browser.get_main_teg(self)\
            .find_elements(By.CSS_SELECTOR, 'div>div:nth-of-type(3)>table>tbody>tr:nth-of-type(1)>td:nth-of-type(2)')
        for i in web_element_coins_profit:
            list_of_coins_profit.append(i)
        return list_of_coins_profit

    def get_dict_with_data(self):
        dict_with_data = {}
        for i, j in zip(self.get_list_of_names_coins(), self.get_list_of_coins_profit()):
            dict_with_data[i.text] = j.text.strip(('$'))
        return dict_with_data

    def get_sorting_dict(self):
        sorted_dict = sorted(self.get_dict_with_data().items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_dict)

    def converting_to_string_format(self, card):
        result = card + ' ' + str(self.get_sorting_dict())
        return result


def main_function():
    cards = ['1080', '5600XT', '5700']
    data_of_coins = Browser()
    for i in cards:
        data_of_coins.get_driver_url(i)
        data_of_coins.exclude_nice_hash()
        yield data_of_coins.converting_to_string_format(i)
    data_of_coins.selenium_driver_close()




if __name__ == '__main__':
    main_function()