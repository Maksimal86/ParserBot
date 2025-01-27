# -*- coding: utf-8 -*-
import time, datetime
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from PIL import Image
from Selenium_Driver import get_driver_selenium


def get_url(driver):
    return 'https://woolypooly.com/en/coin/clore/wallet/AchPZxKXt1fL9G9kbyX3TVFjhnPRmHZF5Q'


def get_right_page(driver):
    print('run right page')
    driver.get(get_url(driver))


def get_quantity_of_miners(driver):
    pass


def get_mgn_hashrate(driver):
    pass


def get_hashrate_30_min(driver):
    pass


def get_hashrate_3_hours(driver):
    pass


def get_hashrate_24_hours(driver):
    pass


def get_revenue(driver):
    pass


def get_graphic_of_hashrate(driver):
    pass


def get_full_screenshort(driver):
    driver.save_screenshot('Wooly_Polly.png')
    return Image.open('Wooly_Polly.png')


def get_part_of_screenshort(driver):
    full_image = get_full_screenshort(driver)
    x = 460  # Начальная координата по X
    y = 200  # Начальная координата по Y
    width = 940  # Ширина области
    height = 720  # Высота области
    return full_image.crop((x, y, x + width, y + height))


def main():
    driver = get_driver_selenium()
    get_right_page(driver)
    time.sleep(5)
    graphic_HR = get_part_of_screenshort(driver)
    graphic_HR.save('graphic_HR.png')
    driver.quit()

if __name__ == '__main__':
    main()


