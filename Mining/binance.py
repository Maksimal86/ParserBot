# -*- coding: utf-8 -*-

import sys
import time, datetime
from bs4 import BeautifulSoup
from selenium.webdriver import Keys, ActionChains
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.actions.mouse_button import MouseButton

def bin():
    s = Service(executable_path=r'C:\yandexdriver.exe')# расположение драйвера
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") # скрытый запуск браузера
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 YaBrowser/22.11.5.715 Yowser/2.5 Safari/537.36') # меняем заголовок запроса
    prefs = {"profile.managed_default_content_settings.images": 2}#не загружаем картинки
    options.add_experimental_option('prefs', prefs) #не загружаем картинки
    driver = webdriver.Chrome(service=s,options=options)
    #driver.implicitly_wait(0.5) # ожидание загрузки
    coins = []
    try:
        for page in [1,2,3]:
            url=f'https://www.binance.com/en/markets/overview?p={page}'
            print(url)
            driver.get(url)

            res = driver.page_source# получили всё страницу в html

            with open('index.html', 'w', encoding="utf-8", errors='ignore') as file:
                file.write(res)
            with open('index.html', 'r', encoding="utf-8", errors='ignore') as file:
                res=file.read()

            find_coin=['BTC', 'ETH','XRP','ETC','FIL','SKL','ETHW','USDT']
            soup = BeautifulSoup(res, 'lxml')

            for i in soup.findAll('div', class_='css-vlibs4'):
                global delta_coin
                coin=i.find('div', class_='css-1x8dg53').get_text()
                price_coin=i.find('div',class_='css-leyy1t').find('div', class_='css-ydcgk2').find('div').get_text()
                delta_coin=i.find('div',class_='css-leyy1t').find('div', class_='css-18yakpx').find('div').get_text()
                if coin in find_coin:
                    coins.append(coin +' '+ price_coin +' '+ delta_coin)
                    #print(coin +' '+ price_coin +' '+ delta_coin)

                    yield coin, price_coin, delta_coin

    except:
        with open('log.txt', 'a', encoding='utf-8') as log:
            log.write('binance '+str(datetime.datetime.now()) + ' нет соединения '+ str( sys.exc_info())+'\n')
    finally:
        print('finaly binance')
        driver.close()
        driver.quit()

def delta():
    bin()
    yield (int(delta_coin))
if __name__ == '__main__':
    bin()