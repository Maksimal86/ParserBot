# -*- coding: utf-8 -*-
import time, datetime
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from PIL import Image
from selenium.webdriver.common.devtools.v135.fetch import continue_request

from Selenium_Driver import get_driver_selenium


def get_url(driver):
    return 'https://woolypooly.com/en/coin/rvn/wallet/RCwKWFnb1jwytx5EnWNoR6pSyc1AfNNwjN'


def get_right_page(driver):
    print('run right page')
    driver.get(get_url(driver))


def get_main_table(driver):
    return driver.find_element(By.CSS_SELECTOR, "div.card.lightSecondBg.lightFirstShadow")


def get_total_hashrate(driver):
    '''Нашли общий хешрейт'''
    return get_main_table(driver).find_element(By.CSS_SELECTOR, '.tooltip').text


def get_tables_of_rigs(driver):
    '''Получаем список данных о ригах'''
    # for i in driver.find_elements(By.CSS_SELECTOR, '.btmRow.lightLine'):
    #     print(i.text)
    return driver.find_elements(By.CSS_SELECTOR, 'div[data-v-15c35004].btmRow.lightLine')


def get_hashrate_30_min(driver):
    '''список хешрейтов за 30 минут для каждого рига '''
    return driver.find_element(By.CSS_SELECTOR, '.btmCell.btmWideCell.btmBlockCell.lightCardContrast').text


def get_name_of_rigs(driver):
    return driver.find_element(By.CSS_SELECTOR, '.btmMobileValue.btmNameShort').text


def get_full_screenshort(driver):
    driver.save_screenshot('Wooly_Polly.png')
    return Image.open('Wooly_Polly.png')


def get_part_of_screenshort(driver):
    full_image = get_full_screenshort(driver)
    x = 460  # Начальная координата по X
    y = 300  # Начальная координата по Y
    width = 940  # Ширина области
    height = 1000  # Высота области
    return full_image.crop((x, y, x + width, y + height))


def main():
    driver = get_driver_selenium()
    get_right_page(driver)
    time.sleep(2)
    list_of_data = []
    quantity_of_rigs = 0
    for i in get_tables_of_rigs(driver)[1:]:
        try:
            quantity_of_rigs += 1
            print(quantity_of_rigs, i.text)
            name_of_rigs = get_name_of_rigs(i)
            print('name_of_rigs', name_of_rigs)
            hashrate = get_hashrate_30_min(i)
            print('hashrate = ', hashrate)
            list_of_data.append(name_of_rigs + " " + str(hashrate))
            list_of_hashrate = '\n'.join(list_of_data)
        except AttributeError:
                continue
    graphic_HR = get_part_of_screenshort(driver)
    graphic_HR.save('graphic_HR.png')
    driver.quit()
    return list_of_hashrate, quantity_of_rigs


if __name__ == '__main__':
    main()


