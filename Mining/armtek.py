# -*- coding: utf-8 -*-

import inspect
import time, datetime, sys
import traceback
from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import json
import mytoken


def options_add():
    options = webdriver.ChromeOptions()
    user_agent = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) + AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/111.0.0.0 Safari/537.36')
    options.add_argument('user-agent=%s' % user_agent)
    options.add_experimental_option("excludeSwitches", ['enable-automation'])  #  FOR uc
    options.add_argument("--disable-blink-features")  # отключение функций блинк-рантайм
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--headless")  # скрытый запуск браузера
    options.add_argument('--no-sandobox')  # режим песочницы
    options.add_argument('--disable-gpu')  # во избежание ошибок
    options.add_argument('--disable-dev-shm-usage')  # увеличения памяти для хрома
    options.add_argument('--lang=en')
    options.add_experimental_option('useAutomationExtension',False)
    return options


def get_driver_selenium():
    service = Service(executable_path=r'C:\yandexdriver.exe')  # расположение драйвера
    options = options_add()
    return webdriver.Chrome(service=service, options=options)


def get_login():
    return mytoken.loginarm


def get_password():
    return mytoken.passwordarm


def get_timeobject(strtime):
    return datetime.datetime.strptime(strtime, '%H:%M:%S').time()


def get_time_now():
    return datetime.datetime.now().time()


def get_url():
    return 'https://etp.armtek.ru/order/report'


def log_in_armtek(driver):
    print('log in armtek')
    try:
        driver.find_element(By.XPATH, '//*[@id="login"]').clear()
        driver.find_element(By.XPATH, '//*[@id="login"]').send_keys(get_login())
        driver.find_element(By.XPATH,
                            '//*[@id="authNewTemplateFormContainer"]/div/div[1]/div[2]/div/form/div[4]/div[1]/label'
                            '/i[1]')
        '//*[@id="login-btn"]'
        driver.find_element(By.XPATH, '//*[@id="password"]').clear()

        driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(get_password(), Keys.ENTER)
    except NoSuchElementException:
        print('except str64 само зашло')


def get_amount_of_delivery(driver, i):
    try:
        return driver.find_element(By.XPATH, f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/'
                                                                 f'td[12]/div').text
    except NoSuchElementException:
        return None


def get_komment(driver, i):
    try:
        return driver.find_element(By.XPATH,f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[15]/span').text
    except NoSuchElementException:
        return 'комментария нет'


def get_right_page(driver):
    print('run right page')
    driver.get(get_url())


def get_date_of_delivery(driver,i):   # дата поставки из таблицы
    try:
        return driver.find_element(By.XPATH,f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[4]'
                                                                f'/div/div').text
    except NoSuchElementException:
        return None


def get_link_of_factura(driver, i):
    return driver.find_element(By.XPATH,f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[5]/div/a').get_attribute('href') # ссылка на фактуру


def get_times_objects():
    time_object_11_00_00 = get_timeobject('11:00:00')
    time_object_00_00_00 = get_timeobject('00:00:00')
    time_object_05_00_00 = get_timeobject('05:00:00')
    time_object_23_59_59 = get_timeobject('23:59:59')
    return time_object_11_00_00, time_object_00_00_00, time_object_05_00_00, time_object_23_59_59


def select_desired_function(driver):
    time_now = get_time_now()
    time_object_11_00_00, time_object_00_00_00, time_object_05_00_00, time_object_23_59_59 = get_times_objects()
    try:
        if time_now > time_object_11_00_00 and time_now < time_object_23_59_59:
            return get_data_from_11_to_05(driver)
        elif time_now > time_object_00_00_00 and time_now < time_object_05_00_00:
            return  get_data_from_11_to_05(driver)
        elif time_now > time_object_05_00_00 and time_now < time_object_11_00_00:
            return get_data_from_5_to_11(driver)
        else:
            print('str 122 где-то ошибка по времени')
    except TypeError:
        traceback.print_exc()


def get_list_of_spare_parts_by_factura(driver, i):
    return  driver.find_element(By.XPATH, f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[5]').text


def get_date_factura(driver,i):
    time.sleep(10)
    try:
        return driver.find_element(By.XPATH, f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[5]/div/div').text
    except NoSuchElementException:
        return ''


def get_page_with_orders(driver):
    driver.find_element(By.XPATH, '//*[@id="SCRDATE"]').clear()  # первая ячейка даты создания заказа
    driver.find_element(By.XPATH, '//*[@id="SCRDATE"]').send_keys('\uE003' * 10,
                                                                  (date.today() - datetime.timedelta(days=20)).strftime(
                                                                      "%d.%m.%Y"), Keys.ENTER)


def check_delivery_date(driver, i):   #всегда возвращается False
    print("run check_delivery_date" )
    date_of_delivery = get_date_of_delivery(driver, i)
    try:
        print('inspect.stack()[1][3] =', inspect.stack()[1][3])
        if inspect.stack()[1][3] == 'get_data_about_upcomming_delivery':
            if (date.today() - datetime.timedelta(days=1)).strftime("%d.%m.%Y") == \
                    date_of_delivery and get_date_factura(driver, i) is None or \
                    date.today().strftime("%d.%m.%Y") == date_of_delivery and get_date_factura(driver, i) is None:
                return True
            else:
                return False
        elif inspect.stack()[1][3] == 'get_data_from_5_to_11':
            if date.today().strftime("%d.%m.%Y") == get_date_factura(driver, i):
                print(True)
                return True
    except NoSuchElementException:
        print(sys.exc_info())
        return False


def check_right_page(driver):
    try:
        if driver.find_element(By.XPATH, '//*[@id="collapseForm"]/div/div[2]/div[1]/span').text != 'Тип заказа':
            return True
    except NoSuchElementException:
        return False


def log_in_click_button(driver):
    driver.find_element(By.XPATH, '//*[@id="login-btn"]').click()


def get_data_about_upcomming_delivery(driver):
    print('run get_data_about_upcomming_delivery ')
    get_page_with_orders(driver)
    time.sleep(5)
    list_of_delivery = []
    try:
        for i in range(1,15):
            amount_of_delivery = get_amount_of_delivery(driver, i)
            if check_delivery_date(driver, i) == True:
                print('check_delivery_date()  == True')
                get_amount_of_delivery(driver,i)
                komment = get_komment(driver,i)
                list_of_delivery.append('Сумма: ' + amount_of_delivery + 'руб, комментарий: ' + komment)
                print(amount_of_delivery, '\n', komment)
            else:
                print('check_delivery_date() == False')
                continue
        if list_of_delivery == []:
            return []
        else:
            print((list_of_delivery))
            return list_of_delivery
    except:
        print('Error str200')
        traceback.print_exc()


def get_coockie(driver):
    print('run armtek_cookie()')
    log_in_armtek(driver)
    time.sleep(4)
    if driver.current_url != get_url():
        get_coockie(driver)
    cookies=driver.get_cookies()
    with open('sess.txt', 'w') as file:
        json.dump(cookies,file)
    time.sleep(4)


def set_data_and_click_on_get_button(driver):
    driver.find_element(By.XPATH, '//*[@id="SCRDATE"]').clear()  # первая ячейка даты создания заказа
    driver.find_element(By.XPATH, '//*[@id="SCRDATE"]').send_keys('\uE003' * 10,
                                                                  (date.today() - datetime.timedelta(days=20)).strftime(
                                                                      "%d.%m.%Y"), Keys.ENTER)


def get_rejected_positions(driver,i):
    return driver.find_element(By.XPATH, f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[2]/img')


def get_date_of_order(driver, i):
    return driver.find_element(By.XPATH, f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[3]/div/div/text()')


def check_date_of_order(driver, i):
    try:
        if get_date_of_order(driver, i) == date.today().strftime("%d.%m.%Y"):
            return True
        else:
            return False
    except NoSuchElementException:
        return False


def check_for_rejected_positions(driver, i):
    try:
        if get_rejected_positions(driver, i):
            return True
    except NoSuchElementException:
        return False


def get_information_about_refusals(driver):
    print('get_information_about_refusals')
    for i in range(1,10):
        if check_for_rejected_positions(driver, i) and  check_date_of_order(driver, i):
            message = 'Отказ' + get_komment(driver, i)
        else:
            message = "Отказов нет"
        return message


def check_and_add_no_delivery(list_of_delivery):
    if list_of_delivery == []:
        list_of_delivery.append('Пока поставка не сформирована')
        print('Поставок нет')


def get_data_from_5_to_11(driver):
    print('run get_data_from_5_to_11')
    if check_right_page(driver) == False:
        get_coockie(driver)
    else:
        list_of_delivery=[]
        try:
            set_data_and_click_on_get_button(driver)
            # парсим 10 строк в заказах
            for i in range(1,10):
                if check_delivery_date(driver, i) == True:
                    print(check_delivery_date(driver,i))
                    driver.get(get_link_of_factura(driver, i))
                    # парсим 15 строк в фактуре
                    for i in range(1, 15):
                        time.sleep(5)
                        try:
                            spare_parts = get_list_of_spare_parts_by_factura(driver, i)
                            print('запчасти', spare_parts)
                            list_of_delivery.append(spare_parts)
                        except NoSuchElementException:
                            break
            check_and_add_no_delivery(list_of_delivery)
            list_of_delivery.append(get_information_about_refusals(driver))
            print(list_of_delivery)
            return list_of_delivery
        except IndexError:
            print('данных больше нет')
            check_and_add_no_delivery(list_of_delivery)
            return list_of_delivery


def get_data_from_11_to_05(driver):
    print('run get_data_from_11_to_24() ')
    list_of_delivery = get_data_about_upcomming_delivery(driver)
    check_and_add_no_delivery(list_of_delivery)
    list_of_delivery.append(get_information_about_refusals(driver))
    return list_of_delivery


def armtek():
    print(' run armtek')
    driver = get_driver_selenium()
    get_right_page(driver)
    time.sleep(3)
    try:
        with open('sess.txt') as sess:
            cookies = json.load(sess) # забираем куки из файла
        for i in range(len(cookies)):
            driver.add_cookie({'name':cookies[i]['name'], 'value':cookies[i]['value']})
# Куки добавляются именно так, по другому с добавлением всех элемeнтов не работает -
# из каждого словаря из списка словарей берутся значения по ключам 'name' и 'value',
# которые потом попадают в соответствующие словари с этими же ключами и значениями
# остальные данные кук селениум добавляет сам.
        get_right_page(driver)
        if check_right_page(driver) == False:
            print('str 279 get_coockie()')
            get_coockie(driver)
        time.sleep(5)
        return select_desired_function(driver)
    except:
        driver.close()
        traceback.print_exc()
    finally:
        driver.quit()

if __name__ == '__main__':
    armtek()