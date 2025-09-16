# -*- coding: utf-8 -*-
from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import time
from selenium.webdriver.common.devtools.v135.fetch import continue_request

from Mining.Selenium_Driver import get_driver_selenium_chrome
from Selenium_Driver import get_driver_selenium_edge
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time


def get_url(driver):
    return 'https://woolypooly.com/en/coin/rvn/wallet/RCwKWFnb1jwytx5EnWNoR6pSyc1AfNNwjN'


def wait_for_page_load(self, driver, timeout=10):
    """
    Ожидает загрузки страницы, используя более надежный подход.
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Используйть Javascript-код для проверки наличия данных на странице.
            js_check = 'return document.readyState === "complete";'
            is_ready = driver.execute_script(js_check)
            if is_ready:
                return  # Страница загрузилась
        except Exception as e:
            print(f"Ошибка при проверке загрузки: {e}")
        time.time()
        time.sleep(0.5)  # Важно: добавление паузы, чтобы не перегружать сервер

    raise TimeoutException(f"Страница не загрузилась за {timeout} секунд.")


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
    print('name',driver.find_element(By.CSS_SELECTOR, '.btmMobileValue.btmNameShort').text)
    return driver.find_element(By.CSS_SELECTOR, '.btmMobileValue.btmNameShort').text


def get_full_screenshort(driver):
    driver.execute_script("window.scrollBy(0, 100);")
    driver.save_screenshot('Wooly_Polly.png')
    return Image.open('Wooly_Polly.png')


def get_part_of_screenshort(driver):
    full_image = get_full_screenshort(driver)
    x = 500 # Начальная координата по X
    y = 250  # Начальная координата по Y
    width = 940  # Ширина области
    height = 600 # Высота области
    return full_image.crop((x, y, x + width, y + height))


def close_bonus(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, 'path').click()
    except NoSuchElementException:
        pass

def main():
    driver = get_driver_selenium_chrome()
    get_right_page(driver)
    close_bonus(driver)
    # wait_for_page_load(driver)
    list_of_data = []
    quantity_of_rigs = 0
    list_of_hashrate = []
    time.sleep(5)
    graphic_HR = get_part_of_screenshort(driver)
    graphic_HR.save('graphic_HR.png')
    for i in get_tables_of_rigs(driver)[1:]:
        try:
            quantity_of_rigs += 1
            print(quantity_of_rigs, i.text)
            name_of_rigs = get_name_of_rigs(i)
            print('name_of_rigs', name_of_rigs)
            hashrate = get_hashrate_30_min(i)
            print('hashrate = ', hashrate)
            list_of_data.append(name_of_rigs + " = " + str(hashrate))
            list_of_hashrate = '\n'.join(list_of_data)
            print(list_of_hashrate)
        except AttributeError:
                continue
    print('driver.quit()')
    driver.quit()
    return list_of_hashrate, quantity_of_rigs


if __name__ == '__main__':
    main()
