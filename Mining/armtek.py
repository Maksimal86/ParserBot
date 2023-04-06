# -*- coding: utf-8 -*-
import sys
import time, datetime
from datetime import date
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import mytoken
def options_add():

    options = webdriver.ChromeOptions()
    user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) + AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36')
    options.add_argument('user-agent=%s' % user_agent)
    options.add_experimental_option("excludeSwitches", ['enable-automation'])  #  FOR uc
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

    return options

def armtek_coockie():
    password=mytoken.passwordarm
    login=mytoken.loginarm
    print('run armtek_coockie()')
    s = Service(executable_path=r'C:\yandexdriver.exe')  # расположение драйвера
    options = options_add()
    driver = webdriver.Chrome(service=s, options=options)
    url='https://etp.armtek.ru/order/report'
    driver.get(url)
    time.sleep(5)
    driver.find_element(By.XPATH, '//*[@id="login"]').send_keys(login)
    driver.find_element(By.XPATH,'//*[@id="authNewTemplateFormContainer"]/div/div[1]/div[2]/div/form/div[4]/div[1]/label/i[1]').click()
    driver.find_element(By.XPATH,'//*[@id="password"]').send_keys(password,Keys.ENTER)
    time.sleep(10)
    driver.refresh()
    time.sleep(2)
    kuki=driver.get_cookies()
    with open('sess.txt', 'w') as file:
        json.dump(kuki,file)
    time.sleep(10)

    return data(driver)
def data(driver): # получаем список поставок
    print('run data cookie')
    driver.find_element(By.XPATH,'//*[@id="SCRDATE"]').clear() # первая ячейка даты создания заказа
    driver.find_element(By.XPATH, '//*[@id="SCRDATE"]').send_keys('\uE003'*10,(date.today()- datetime.timedelta(days=20)).strftime("%d.%m.%Y"), Keys.ENTER)
    time.sleep(5)
    list_z=[]
    try:
        for i in range(1,10):
            s=driver.find_element(By.XPATH, f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[12]/div').text # сумма поставки
            kom=driver.find_element(By.XPATH,f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[15]/span').text # комментарий
            if driver.find_element(By.XPATH,f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[4]/div/div').text ==date.today().strftime("%d.%m.%Y"):# дата поставки
                list_z.append('Сумма: '+s+'руб, комментарий: '+kom)
                print(s,'\n',kom)
    except:
        print(sys.exc_info())
        print('Поставок больше нет')
    print(list_z)
    return list_z

def armtek():
    print(' run armtek')
    options = options_add()
    s = Service(executable_path=r'C:\yandexdriver.exe')  # расположение драйвера
    driver = webdriver.Chrome(service=s, options=options)
    url='https://etp.armtek.ru/order/report'
    driver.get(url)
    time.sleep(5)
    try:
        #driver.refresh() # перезагружаем для того, чтобы добавить куки
        time.sleep(3)
        with open('sess.txt') as sess:
            kuk=json.load(sess) # забираем куки из файла
            print(kuk)
        k=driver.get_cookies()
        print(k)
        for i in range(len(kuk)):
            driver.add_cookie({'name':kuk[i]['name'], 'value':kuk[i]['value']})
       # Куки добавляются именно так, по другому с добавлением всех элемнтов не работает -
       # из каждого словаря из списка словарей берутся значения по ключам 'name' и 'value',
       # которые потом попадают в соответствующие словари с этими же ключами и значениями
       # остальные данные кук селениум добавляет сам.
        driver.get(url)
        time.sleep(5)
        print('return data driver')
        return data(driver)
    except:
        driver.close()
        print(sys.exc_info())
        print('armtek except')
        armtek_coockie() # получили куки, записали в файл и вернули список с поставками
        time.sleep(2)
    finally:
        driver.quit()

if __name__ == '__main__':
    armtek()


