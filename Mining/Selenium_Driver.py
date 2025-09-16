# -*- coding: utf-8 -*-

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
import inspect

def set_options_of_selenium():
    firefox_path = r"C:\Program Files (x86)\Mozilla Firefox\firefox.exe"
    calling_function =inspect.currentframe().f_back.f_code.co_name
    print('вызывающая функция =', calling_function)
    if inspect.currentframe().f_back.f_code.co_name == 'get_driver_selenium_chrome':
        options = webdriver.ChromeOptions()
    elif inspect.stack()[1] == 'get_driver_selenium_edge':
        options = webdriver.EdgeOptions()
    elif inspect.stack()[1] == 'get_service_selenium_firefox()':
        options = webdriver.FirefoxOptions()
        options.binary_location = firefox_path
    else:
        return None
    # options.add_argument("--headless")  # скрытый запуск браузера
    options.add_argument("--start-maximized")
    options.headless = True
    return options


def get_service_selenium_chrome():
    service =  ChromeService(executable_path='C:/chromedriver.exe')
    print(vars(service))
    return service


def get_service_selenium_edge():
    return ChromeService(executable_path='C:/msedgedriver.exe')


def get_service_selenium_firefox():
    return FirefoxService(executable_path='C:/geckodriver.exe')


def get_driver_selenium_chrome():
    """ для хрома"""
    chrome_path = r'C:\chrome-win64\chrome.exe'
    service = get_service_selenium_chrome()
    options = set_options_of_selenium()
    options.binary_location =chrome_path
    print(options.to_capabilities())
    return webdriver.Chrome(service=service, options=options)


def get_driver_selenium_edge():
    """ для edge"""
    service = get_service_selenium_edge()
    options = set_options_of_selenium()
    return webdriver.Edge(options=options, service=service)


def get_driver_selenium_firefox():
    """ для firefox"""
    firefox_path = r"C:\Program Files(x86)\Mozilla Firefox\firefox.exe"
    service = get_service_selenium_firefox()
    options = set_options_of_selenium()
    return webdriver.Firefox(options=options, service=service)

