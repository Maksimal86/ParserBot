# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
from json import JSONDecodeError
import time, datetime, sys
import traceback
from datetime import date
from selenium.webdriver.common.by import By
from selenium.common import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from Selenium_Driver import get_driver_selenium_edge
import json
import mytoken


class Basic(ABC):
    def __init__(self):
        # self.options =Selenium_Driver.set_options_of_selenium()
        # print(self.options)
        self.driver = get_driver_selenium_edge()
        self.login = mytoken.loginarm
        self.password = mytoken.passwordarm
        self.url = 'https://etp.armtek.ru/order/report'
        self.number_of_lines = 25  # количество строк в документе, подлежащее сбору информации


    def wait_for_page_load(self, timeout=7):
        """
        Ожидает загрузки страницы, используя более надежный подход.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                js_check = 'return document.readyState === "complete";'
                is_ready = self.driver.execute_script(js_check)
                if is_ready:
                    return  # Страница загрузилась
            except Exception as e:
                print(f"Ошибка при проверке загрузки: {e}")
            time.sleep(0.5)
        raise TimeoutException(f"Страница не загрузилась за {timeout} секунд.")


    def set_cookies(self):
        """
                 Куки добавляются именно так, по другому с добавлением всех элемeнтов не работает -
         из каждого словаря из списка словарей берутся значения по ключам 'name' и 'value',
         которые потом попадают в соответствующие словари с этими же ключами и значениями
         остальные данные кук селениум добавляет сам.
        :return:
        """
        time.sleep(5)
        print('run set_cookies')
        try:
            with open('sess.txt') as sess:
                cookies = json.load(sess)  # забираем куки из файла
            k = self.driver.get_cookies()
            print(k)
            for i in range(len(cookies)):
                self.driver.add_cookie({'name': cookies[i]['name'], 'value': cookies[i]['value']})
        except JSONDecodeError:
            Basic.write_of_cookies_in_file(self)


    def write_of_cookies_in_file(self):
        """получаем куки, и записываем их в файл для того, чтобы входить без капчи"""
        print("run write_of_cookies_in_file")
        self.driver.refresh()
        cookies = self.driver.get_cookies()
        with open('sess.txt', 'w') as file:
            json.dump(cookies, file)
        # time.sleep(4)


    def log_in_armtek(self):
        """
        осуществляем вход в аккаунт
        :return: None
        """
        print('log in armtek')
        try:
            login_field = self.driver.find_element(By.XPATH, '//*[@id="login"]')
            login_field.clear()
            time.sleep(1)
            login_field.send_keys(self.login)
            time.sleep(1)
            self.driver.find_element(By.XPATH,
                                     '//*[@id="authNewTemplateFormContainer"]/div/div[1]/div[2]/div/form/div[4]/div[1]'
                                     '/label/i[1]')
            password_field = self.driver.find_element(By.XPATH,'//*[@id="password"]')
            password_field.clear()
            time.sleep(1)
            password_field.send_keys(self.password, Keys.ENTER)
            time.sleep(5)
        except NoSuchElementException:
            print('except str95 само зашло', sys.exc_info())


    def get_right_page(self):
        """
        заходим на нужную страницу
        :return: None
        """
        self.driver.get(self.url)


    def check_right_page(self):
        """
        Проверяем - действительно ли мы на нужной странице
        :return: True
        """
        try:
            self.wait_for_page_load()
            if self.driver.find_element(By.XPATH, '//*[@id="switch-design"]').text != 'Старый дизайн':
                return True
        except NoSuchElementException:
            print(sys.exc_info())
            return False


    def set_date_of_orders(self):
        """
        задаем количество дней days, за которое выводится список заказов
        и формируем этот список нажатием enter
        :return None
        """
        print('set_date_of_orders')
        days = 10
        self.driver.find_element(By.XPATH, '//*[@id="SCRDATE"]').clear()  # первая ячейка даты создания заказа
        self.driver.find_element(By.XPATH, '//*[@id="SCRDATE"]').send_keys('\uE003' * days,
                                                                           (date.today() - datetime.timedelta(
                                                                               days=days)).strftime(
                                                                               "%d.%m.%Y"), Keys.ENTER)


    def get_order_list_strings(self):
        """получаем строки с заказами"""
        list_of_string = self.driver.find_elements(By.CSS_SELECTOR, 'tr[role].even, tr[role].odd')
        return list_of_string


    def get_order_date(self, order_line):
        """передавая строку с заказом, ищем в ней дату заказа """
        order_date = order_line.find_elements(By.CSS_SELECTOR, 'td.text-center')[3].find_element(By.CSS_SELECTOR,
                                                                                                 'div.nowrap>div').text
        return order_date

# не печатается дата фактуры

    def get_order_data_cells(self, order_line):
        """Получаем ячейки данных из строки заказа"""
        data_cells = order_line.find_elements(By.CSS_SELECTOR, 'td')
        return data_cells


    def find_rejected_positions(self, order_line):
        """
        находим отказные позиции
        :param order_line: строка с заказом
        :return: text
        """
        try:
            order_line.find_element(By.CSS_SELECTOR, "td>img[title='Все позиции отклонены']")
            order_date = self.get_order_date(order_line)
            return True, order_date
        except NoSuchElementException:
            try:
                order_line.find_element(By.CSS_SELECTOR,
                                               "td>img[title='Имеются частично  поставленные и отклоненные позиции']")
                order_date = self.get_order_date(order_line)
                return True, order_date
            except NoSuchElementException:
                print('False reject')
                return False, None


    @staticmethod
    def record_comment(comment):
        """
        Записываем комментарий об отказе в файл, если его там нет
        :return: True, None
        """
        with open('armtek.txt', 'r+', encoding='utf-8' ) as f:
            rejected_strings = f.readlines()
            if comment in rejected_strings:
                print('возврат уже зафиксирован')
                return None
            else:
                f.write(comment)
                return True


    def get_delivery_amount(self,order_line):
        """
        Получаем сумму поставки
        :param order_line: строка с заказом
        :return:str сумма
        """
        try:
            delivery_amount = self.get_order_data_cells(order_line)[12].text
            print('сумма поставки = ',delivery_amount)
            return delivery_amount
        except NoSuchElementException:
            return ''


    def get_сomment(self, order_line):
        """
        Получаем комментарий поставки
        :param order_line: строка с заказом
        :return:str комментарий
        """
        try:
            comment = self.get_order_data_cells(order_line)[14].text
            print('комментарий - ', comment)
            return comment
        except NoSuchElementException:
            print('комментария нет')
            return 'комментария нет'  #?????


    def get_delivery_date(self, order_line):
        """
        Получаем дату поставки
        :param order_line: строка с заказом
        :return:str комментарий
        """
        try:
            delivery_date = (self.get_order_data_cells(order_line)[4].find_element
                             (By.CSS_SELECTOR,'img[title = "Дата создания поставки"]').text)
            print('дата поставки = ', delivery_date)
            return delivery_date
        except NoSuchElementException:
            return None


    def get_invoice_date(self, order_line):
        """
        получаем дату создания фактуры
        :param order_line: строка с заказом
        :return: str дата
        """
        try:
            invoice_date = self.get_order_data_cells(order_line)[5].find_element(By.CSS_SELECTOR, 'img[title = "Дата создания фактуры"]').text
            print('дата фактуры = ', invoice_date)
            return invoice_date
        except NoSuchElementException:
            return None


    def get_link_of_invoice(self, order_line):
        """
        Получаем ссылку на фактуру
        :param order_line: строка с заказом
        :return: href
        """
        link = (self.get_order_data_cells(order_line)[5]
                .find_element(By.CSS_SELECTOR, "div>img[title='Номер фактуры']+a").get_attribute('href'))
        print('linK=', link)
        return link

#  нужна ли?
    def check_date_of_order(self, order_line):
        """
        Проверяем соответствие даты заказа сегодняшней дате
        :param order_line: строка с заказом
        :return: True
        """
        delta = datetime.timedelta(days=1)
        try:
            if self.get_order_date(order_line) == '27.09.2025':
                # if self.get_date_of_order(order_line) == date.today().strftime("%d.%m.%Y"):
                return True
            else:
                return False
        except NoSuchElementException:
            return False


    def change_of_organization(self):
        self.driver.find_element(By.ID, 'kunnrRgLink').click()
        self.driver.find_element(By.ID, 'kunnrRgMenu').click()


    @abstractmethod
    def check_date_of_delivery(self, i, date_of_delivery):
        pass


    @abstractmethod
    def get_data(self):
        pass


class MorningRequest(Basic):
    def check_date_of_delivery(self, order_line, date_of_delivery):
        """описываются условия выбора заказов по необходимой дате,
        если дата фактуры сегодняшняя
        :param order_line: строка с заказом
        :param date_of_delivery:
        :return: True
        """
        print('run check_date_of_delivery morning')
        try:
            if (date.today() - datetime.timedelta(days=1)).strftime("%d.%m.%Y") == self.get_invoice_date(order_line):
                print('Дата поставки - True')
                return True
            else:
                print('Дата поставки - False')
        except NoSuchElementException:
            print(sys.exc_info())
            return False


    def get_spare_parts_by_invoice(self):
        """
        получаем наименование запчасти в фактуре
        :return: str запчасть
        """
        strings_spare_parts = self.get_order_list_strings()
        data_cells = self.get_order_data_cells(strings_spare_parts)
        spare_parts = data_cells[4].text
        print('spare_parts = ', spare_parts)
        return spare_parts
################## добавить артикул в вывод

    def get_data(self):
        """
        Собираем в единых список сумму и все комментарии предстоящих поставок
        :return: список поставок
        """
        print('run get_data')
        list_of_delivery = []
        self.set_date_of_orders()
        time.sleep(7)
        for order_line in self.get_order_list_strings():
            invoice_date = self.get_invoice_date(order_line)
            comment = self.get_сomment(order_line)
            rejected_positions = self.find_rejected_positions(order_line)
            print('rejected_positions = ', rejected_positions)
            if rejected_positions[0] == True and self.record_comment(comment):
                list_of_delivery.append("Отказ, " + "Заказ от " + rejected_positions[1] + ' ' + comment)
            else:
                continue
            if invoice_date == date.today():
                spare_parts = self.get_spare_parts_by_invoice()
                list_of_delivery.append(spare_parts)
        print('Поставка - ', list_of_delivery)
        return list_of_delivery


class EveningRequest(Basic):
    def check_date_of_delivery(self, i, date_of_delivery):
        """
        описываются условия выбора заказов по необходимы датам
        если дата поставки вчерашняя и даты фактуры нет или она или поставка сегодняшняя, а фактуры нет
        :param i:
        :param date_of_delivery:
        :return: True
        """
        print("run check_date_of_delivery")
        try:
            if (date.today() - datetime.timedelta(days=1)).strftime("%d.%m.%Y") == \
                    date_of_delivery and self.get_invoice_date(i) == '' or \
                    date.today().strftime("%d.%m.%Y") == date_of_delivery and self.get_invoice_date(i) == '':
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
                    komment = self.get_сomment(i)
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
                print('list_of_delivery - ', list_of_delivery)
                return list_of_delivery
        except:
            print('Error str 425')
            self.check_and_add_no_delivery(list_of_delivery)
            traceback.print_exc()


def select_of_class():
    """
    Выбираем какую функцию вызывать в зависимости от времени суток
    :return None
    """
    time_now = datetime.datetime.now().time()
    time_object_12_00_00, time_object_00_00_00, time_object_05_00_00, time_object_23_59_59 = get_times_objects()
    try:
        if time_now > time_object_05_00_00 and time_now < time_object_12_00_00:
            return MorningRequest()
        else:
            return MorningRequest()
    except TypeError:
        traceback.print_exc()



def checking_repeated_message(information_about_refusals):
    """
    проверяем: была ли запись о возврате, а, следовательно, и сообщение
    об этом. Записываем, в файл, если сообщения нет.

    """
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



def get_timeobject(strtime):
    """
    :param strtime:
    :return: timeobject
    """
    return datetime.datetime.strptime(strtime, '%H:%M:%S').time()



def get_times_objects():
    """
    получаем time_object из str
    :return: time_object
    """
    time_object_12_00_00 = get_timeobject('12:00:00')
    time_object_00_00_00 = get_timeobject('00:00:00')
    time_object_05_00_00 = get_timeobject('05:00:00')
    time_object_23_59_59 = get_timeobject('23:59:59')
    return time_object_12_00_00, time_object_00_00_00, time_object_05_00_00, time_object_23_59_59


def main():
    print('run armtek')
    request = select_of_class()
    time.sleep(3)
    try:
        request.get_right_page()
        request.wait_for_page_load()
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
