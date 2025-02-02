# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service



def set_options_of_selenium():
    options = webdriver.ChromeOptions()
    user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) + AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')
    options.add_argument('user-agent=%s' % user_agent)
    options.add_experimental_option("excludeSwitches", ['enable-automation'])  #  FOR uc
    options.add_argument("--disable-blink-features")  # отключение функций блинк-рантайм
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument("--headless")  # скрытый запуск браузера
    options.add_argument('--no-sbtmRow lightLineandobox')  # режим песочницы
    options.add_argument('--disable-gpu')  # во избежание ошибок
    options.add_argument('--disable-dev-shm-usage')  # увеличения памяти для хрома
    # options.add_argument('--disable-brouser-side-navigation')  # прекращение загрузки дополнительных подресурсов при длительной загрузки страницы
    options.add_argument('--lang=en')
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--start-fullscreen")
    return options


def get_service_selenium():
    return Service(executable_path=r'C:/chromedriver.exe')


def get_driver_selenium():
    service = get_service_selenium()
    options = set_options_of_selenium()
    return webdriver.Chrome(service=service, options=options)


