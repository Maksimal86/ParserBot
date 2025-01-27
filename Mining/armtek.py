    # -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from Selenium_Driver import set_options_of_selenium
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



class Basic(ABC):
    def __init__(self):
        self.options = set_options_of_selenium()
        self.service = Service(executable_path=r'C:/chromedriver.exe')
        self.driver = webdriver.Chrome(service=self.service, options=self.options)
        self.login = mytoken.loginarm
        self.password = mytoken.passwordarm
        self.url = 'https://etp.armtek.ru/order/report'
        self.number_of_lines = 25 # количество строк в документе, подлежащее сбору информации


    def set_cookies(self):
        '''
                 Куки добавляются именно так, по другому с добавлением всех элемeнтов не работает -
         из каждого словаря из списка словарей берутся значения по ключам 'name' и 'value',
         которые потом попадают в соответствующие словари с этими же ключами и значениями
         остальные данные кук селениум добавляет сам.
        :return:
        '''
        print('run set_cookies')
        with open('sess.txt') as sess:
            cookies = json.load(sess)  # забираем куки из файла
        k = self.driver.get_cookies()
        print(k)
        for i in range(len(cookies)):
            self.driver.add_cookie({'name': cookies[i]['name'], 'value': cookies[i]['value']})


    def write_of_cookies_in_file(self):
        '''получаем куки, и записываем их в файл для того, чтобы входить без капчи'''
        print("run write_of_cookies_in_file")
        self.driver.refresh()
        cookies = self.driver.get_cookies()
        with open('sess.txt', 'w') as file:
            json.dump(cookies,file)
        time.sleep(4)


    def log_in_armtek(self):
        '''
        осуществляем вход в аккаунт
        :param driver:
        :return: None
        '''
        print('log in armtek')
        try:
            self.driver.find_element(By.XPATH, '//*[@id="login"]').clear()
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//*[@id="login"]').send_keys(self.login)
            time.sleep(1)
            self.driver.find_element(By.XPATH,
                         '//*[@id="authNewTemplateFormContainer"]/div/div[1]/div[2]/div/form/div[4]/div[1]/label'
                                '/i[1]')
            '//*[@id="login-btn"]'
            self.driver.find_element(By.XPATH, '//*[@id="password"]').clear()
            time.sleep(1)
            self.driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(self.password, Keys.ENTER)
            time.sleep(5)
        except NoSuchElementException:
            print('except str72 само зашло', sys.exc_info()) #проверить логику


    def get_right_page(self):
        '''
        заходим на нужную страницу
        :param driver:
        :return: None
        '''
        self.driver.get(self.url)


    def check_right_page(self):
        '''
        Проверяем - действительно ли мы на нужной странице
        :return: True
        '''
        try:
            if self.driver.find_element(By.XPATH, '//*[@id="switch-design"]').text != 'Старый дизайн':
                return True
        except NoSuchElementException:
            print(sys.exc_info())
            return False


    def set_data_of_orders(self):
        """
        задаем количество дней days, за которое выводится список заказов
        и формируем этот список нажатием enter
        :return None
        """
        print('set_data_of_orders')
        days = 10
        self.driver.find_element(By.XPATH, '//*[@id="SCRDATE"]').clear()  # первая ячейка даты создания заказа
        self.driver.find_element(By.XPATH, '//*[@id="SCRDATE"]').send_keys('\uE003' * days,
                                                                      (date.today() - datetime.timedelta(days=days)).strftime(
                                                                           "%d.%m.%Y"), Keys.ENTER)


    def get_information_about_refusals(self, i):
        '''
        Если есть отказные позиции - возвращается message с отказом и комментарием
        :param driver:
        :param i:
        :return: message
        '''
        print('get_information_about_refusals')
        if self.check_rejected_positions(i):
            message = 'Отказ ' + self.get_komment(i)
        else:
            message = ""
        return message


    def get_amount_of_delivery(self, i):
        '''
        Получаем сумму поставки
        :param driver:
        :param i:
        :return:str сумма
        '''
        try:
            return self.driver.find_element(By.XPATH, f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/'
                                                                     f'td[12]/div').text
        except NoSuchElementException:
            return ''


    def get_komment(self, i):
        '''
        Получаем комментарий поставки
        :param driver:
        :param i:
        :return:str комментарий
        '''
        try:
            return self.driver.find_element(By.XPATH,f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[15]/span').text
        except NoSuchElementException:
            return 'комментария нет'



    def get_date_of_delivery(self,i):
        '''
        получаем дату поставки
        :return str дата
        '''
        try:
            return self.driver.find_element(By.XPATH,f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[4]'
                                                                    f'/div/div').text
        except NoSuchElementException:
            return None


    def get_date_factura(self,i):
        '''
        получаем дату создания фактуры
        :param driver:
        :param i:
        :return: str дата
        '''
        time.sleep(1)
        try:
            return self.driver.find_element(By.XPATH,
                                            f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[5]/div/div').text
        except NoSuchElementException:
            print('str 143 NoSuchElementException')
            return ''


    def get_link_of_factura(self,i):
        '''
        Получаем ссылку на фактуру
        :param driver:
        :param i:
        :return: href
        '''
        return (self.driver.find_element(By.XPATH, f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[5]/div/a')
                .get_attribute('href'))


    def check_rejected_positions(self, i):
        '''
         Проверяем наличие отказа в списке поставок можно убрать - оставить только find...
        :return: True
        '''
        text = self.find_text_about_rejected_positions(i)
        if (self.check_date_of_order(i) and text == 'Все позиции отклонены'   or
                text == 'Имеются частично поставленные и отклоненные позиции'):
            print("True reject")
            return True
        else:
            print('False reject')
            return False


    def find_text_about_rejected_positions(self, i):
        '''
        находим текст, говорящий о наличии отказа
        :param driver:
        :param i:
        :return: text
        '''
        try:
            return (self.driver.find_element(By.XPATH, f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[2]/img')
                    .get_attribute('title'))
        except NoSuchElementException:
            print('False reject')
            return False


    def check_date_of_order(self, i):
        '''
        Проверяем соответствие даты заказа сегодняшней дате
        :param driver:
        :param i:
        :return: True
        '''
        try:
            if self.get_date_of_order(i) == date.today().strftime("%d.%m.%Y"):
                return True
            else:
                return False
        except NoSuchElementException:
            return False


    def get_date_of_order(self, i):
        '''
        получаем дату заказа
        :param driver:
        :param i:
        :return: str дата
        '''
        return self.driver.find_element(By.XPATH, f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[3]/div/div').text


    @abstractmethod
    def check_date_of_delivery(self,i):
        pass


    @abstractmethod
    def get_data(self):
        pass


class Morning_request(Basic):
    def check_date_of_delivery(self, i, date_of_delivery):
        '''
        описываются условия выбора заказов по необходимой дате,
        если дата фактуры сегодняшняя
        :param driver:
        :param i:
        :param date_of_delivery:
        :return: True
        '''
        print('run check_date_of_delivery morning')
        try:
            if date.today().strftime("%d.%m.%Y") == self.get_date_factura(i):
                print(True)
                return True
            else:
                print("False")
        except NoSuchElementException:
            print(sys.exc_info())
            return False


    def get_list_of_spare_parts_by_factura(self,i):
        '''
        получаем наименование запчасти в фактуре
        :param driver:
        :param i:
        :return: str запчасть
        '''
        return  self.driver.find_element(By.XPATH, f'//*[@id="DataTables_Table_0"]/tbody/tr[{i}]/td[5]').text


    def get_data(self):
        """
        Собираем в единых список сумму все комментарии предстоящих поставок
        :param driver:
        :return: список поставок
        """
        print('run get_data')
        list_of_delivery = []
        try:
            self.set_data_of_orders()
            for i in range(1, self.number_of_lines):
                date_of_delivery = self.get_date_of_delivery(i)
                delivery_data = self.check_date_of_delivery(i,date_of_delivery)
                rejected_positions = self.check_rejected_positions(i)
                if delivery_data or rejected_positions:
                    print(delivery_data)
                    self.driver.get(self.get_link_of_factura(i))
                    list_of_delivery.append(self.get_information_about_refusals(i))
                    for i in range(1, self.number_of_lines):
                        time.sleep(3)
                        try:
                            spare_parts = self.get_list_of_spare_parts_by_factura(i)
                            print('запчасти', spare_parts)
                            list_of_delivery.append(spare_parts)
                        except NoSuchElementException:
                            break
                else:
                    continue
            print(list_of_delivery)
            return list_of_delivery
        except IndexError:
            print('данных больше нет')
            return list_of_delivery


class Evening_request(Basic):
    def check_date_of_delivery(self, i, date_of_delivery):
        '''
        описываются условия выбора заказов по необходимы датам
        если дата поставки вчерашняя и даты фактуры нет или она или поставка сегодняшняя, а фактуры нет
        :param driver:
        :param i:
        :param date_of_delivery:
        :return: True
        '''
        print("run check_date_of_delivery")
        try:
            if (date.today() - datetime.timedelta(days=1)).strftime("%d.%m.%Y") == \
                    date_of_delivery and self.get_date_factura(i) == '' or \
                    date.today().strftime("%d.%m.%Y") == date_of_delivery and self.get_date_factura(i) == '':
                print('True')
                return True
            else:
                print("False")
                return False
        except NoSuchElementException:
            print(sys.exc_info())
            return False


    @staticmethod
    def check_and_add_no_delivery(list_of_delivery):
        """
        Проверяем наличие поставки, если список поставки пуст - вставляем в список выражение об этом
        :param list_of_delivery:
        :return: None
        """
        if list_of_delivery == []:
            list_of_delivery.append('Пока поставка не сформирована')
            print('Поставок нет')


    def get_data(self):
        """
        Собираем в единых список сумму по предстоящей поставке и комментарий к ней
        number of lines - количество просматриваемых строк в списке заказов
        :param driver:
        :return: список ЗЧ в поставке
        """
        print('run get_data Morning class ')
        self.set_data_of_orders()
        time.sleep(1)
        list_of_delivery = []
        try:
            for i in range(1, self.number_of_lines):
                information_about_refusals = self.get_information_about_refusals(i)
                ''' отказы выводятся как только они появились, поэтому не подлежат проверке
                по дате check_delivery_date'''
                if not checking_repeated_message(information_about_refusals):
                    list_of_delivery.append(information_about_refusals)
                date_of_delivery = self.get_date_of_delivery(i)
                if self.check_date_of_delivery(i, date_of_delivery):
                    amount_of_delivery = self.get_amount_of_delivery(i)
                    komment = self.get_komment(i)
                    list_of_delivery.append('Сумма: ' + amount_of_delivery + 'руб, комментарий: ' + komment)
                    print(amount_of_delivery, '\n', komment)
                else:
                    continue
            self.check_and_add_no_delivery(list_of_delivery)
            if list_of_delivery == []:
                list_of_delivery.append('Пока поставка не сформирована')
                print('Поставок нет')
                return []
            else:
                print('list_of_delivery - ', (list_of_delivery))
                return list_of_delivery
        except:
            print('Error str 425')
            self.check_and_add_no_delivery(list_of_delivery)
            traceback.print_exc()


def select_of_class():
    '''
    Выбираем какую функцию вызывать в зависимости от времени суток
    :return None
    '''
    time_now = datetime.datetime.now().time()
    time_object_12_00_00, time_object_00_00_00, time_object_05_00_00, time_object_23_59_59 = get_times_objects()
    try:
        if time_now > time_object_05_00_00 and time_now < time_object_12_00_00:
            return Evening_request()# поменять
        else:
            return Evening_request()
    except TypeError:
        traceback.print_exc()


@staticmethod
def checking_repeated_message(information_about_refusals):
    '''
    проверяем: была ли запись о возврате, а, следовательно, и сообщение
    об этом. Записываем, в файл, если сообщения нет.
    :param driver:
    :param i:
    :return: True
    '''
    print('refaulse = ', information_about_refusals)
    if information_about_refusals:
        print("есть информация об отказах")
        with open('armtek.txt', 'r+', encoding='cp1251') as file:
            # print('file = ', file.read())
            if information_about_refusals + '\n' in file.readlines():
                return True
            else:
                file.write(information_about_refusals + '\n')
                return False


@staticmethod
def get_timeobject(strtime):
    '''
    :param strtime:
    :return: timeobject
    '''
    return datetime.datetime.strptime(strtime, '%H:%M:%S').time()

@staticmethod
def get_times_objects():
    '''
    получаем time_object из str
    :return: time_object
    '''
    time_object_12_00_00 = get_timeobject('12:00:00')
    time_object_00_00_00 = get_timeobject('00:00:00')
    time_object_05_00_00 = get_timeobject('05:00:00')
    time_object_23_59_59 = get_timeobject('23:59:59')
    return time_object_12_00_00, time_object_00_00_00, time_object_05_00_00, time_object_23_59_59


def main():
    print('run armtek')
    request  = select_of_class()
    time.sleep(3)
    try:
        request.get_right_page()
        request.set_cookies()
        '''повторный вызов нужен для того, чтобы применить куки'''
        request.get_right_page()
        if request.check_right_page() == False:
            request.log_in_armtek()
            time.sleep(3)
            if request.check_right_page() == False:
                print('Не вошли в Армтек')
                return ['Не вошли в Армтек']
        request.write_of_cookies_in_file()
        return request.get_data()
    except:
        request.driver.close()
        traceback.print_exc()
    finally:
        request.driver.quit()


if __name__ == '__main__':
    main()



