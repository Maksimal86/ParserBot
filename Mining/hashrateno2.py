# -*- coding: utf-8 -*-
import time, datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
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

def hasrateno():
    s = Service(executable_path=r'C:\yandexdriver.exe')  # расположение драйвера
    #s=Service(executable_path=r'C:\chromedriver.exe')
    options = options_add()
    driver = webdriver.Chrome(service=s, options=options)
    cards = ['1080','5600XT','5700']  # список нужных карт
    quant=0 # счетчик типов карт
    quantity_res = 14 # количество выводимых монет для каждой карты
    sum_max_profit=0
    big_list=[]# общий список для return
    for card in cards: # перебираем страницы с разными картами
        result_coin = 0
        quant+=1
        url = f'https://www.hashrate.no/gpus/{card}'
        driver.get(url)
        with open('hrn.html', 'w', encoding='utf-8', errors='ignore') as file:
            file.write(driver.page_source)
        # убираем из подбора найсхеш
        driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div[2]/div[2]/div[2]/form[2]/div[3]/div[2]/div/input').click()
        time.sleep(3)
        # Находим тег, который является родителем для всех тегов, в которых находятся монеты и их профит.
        teg_coin = driver.find_element(By.XPATH, '/html/body/div/div[2]/div[2]/div[2]/div[2]/div[3]')
        coin_names=teg_coin.find_elements(By.CLASS_NAME, 'deviceHeader')
        profits=teg_coin.find_elements(By.XPATH,'div/a/div/div[3]/table/tbody/tr[3]/td[2]')
        coin=[]
        prof_list=[]
        if card == '5700':
            quantity_cards = 7  # количество карт для вывода суммы профита
        elif card == '5600XT':
            quantity_cards = 22
        elif card == '1080':
            quantity_cards = 8
        elif card == '1070':
            quantity_cards = 4
        elif card == '1060':
            quantity_cards = 5
        else:
            quantity_cards = 1
        for coin_name in coin_names[:-1]:
            coin.append(coin_name)

        for profit in profits[:-1]:
            prof_list.append(profit)
        dict_coin_profit={c.text:p.text for c,p in zip(coin,prof_list)} # словарь с ключом по имени монеты
        sort_list_key=sorted(dict_coin_profit, key=dict_coin_profit.get, reverse=True)# получили список ключей, отсортированных по значениям
        sort_list=[]
        sort_dict={}
        for key in sort_list_key:
            sort_dict[key]=dict_coin_profit[key]
        max_profit = round(float(list(sort_dict.values())[0][1:]) * quantity_cards,1)
        sum_max_profit+=max_profit
        for key, value in sort_dict.items():
            result_coin+=1
            sort_list.append(key+':'+str(round(float(value[1:])*quantity_cards,2))+'$')
            if result_coin == quantity_res:
                break
        sort_list.append('Max profit='+str(round(max_profit,1))+'$')
        if quant == len(cards):
            sort_list.append('Суммарный максимальный профит='+str(sum_max_profit)+'$')
        big_list.append(card+' '+str(sort_list))
        for i in big_list:
            print (str(i).translate({ord(i):None for i in "[]'"}))
    return big_list

if __name__ == '__main__':
    hasrateno()
