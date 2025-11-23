import datetime
import json
import sys
import time
import mytoken
from abc import ABC, abstractmethod
from datetime import date, timedelta
from json import JSONDecodeError
from selenium.common import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from Selenium_Driver import get_driver_selenium_chrome
from Selenium_Driver import get_driver_selenium_edge


class Basic(ABC):
    """
    Основной класс
    """

    def __init__(self):
        self.comment = None
        self.driver = get_driver_selenium_chrome()
        self.login = mytoken.loginarm
        self.password = mytoken.passwordarm
        self.url = 'https://etp.armtek.ru/order/report'
        self.number_of_lines = 25  # количество строк в документе, подлежащее сбору информации

    def wait_for_page_load(self, timeout=12):
        """
        Ожидает загрузки страницы, используя более надежный подход.
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                js_check = 'return document.readyState === "complete";'
                is_ready = self.driver.execute_script(js_check)
                if is_ready:
                    return True
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
        :return: None
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
            password_field = self.driver.find_element(By.XPATH, '//*[@id="password"]')
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
            if self.driver.find_element(By.CSS_SELECTOR, 'a.collapse-link-text').text == 'Фильтр отчета по заказам':
                return True
        except NoSuchElementException:
            print(sys.exc_info())
            return False

    def set_date_of_orders(self, days=20):
        """
        Устанавливаем количество дней days, за которое выводится список заказов,
        начиная с сегодняшней даты,
        и формируем этот список нажатием enter
        Args:
        days (int, optional): Количество дней для вывода списка заказов. По умолчанию 20.
        :return None
        """
        print('set_date_of_orders')
        self.driver.find_element(By.XPATH, '//*[@id="SCRDATE"]').clear()  # первая ячейка даты создания заказа
        self.driver.find_element(By.XPATH, '//*[@id="SCRDATE"]').send_keys('\uE003' * days,
                                                                           (date.today() - datetime.timedelta(
                                                                               days=days)).strftime(
                                                                               "%d.%m.%Y") + Keys.ENTER)

    def get_strings(self):
        """получение строк заказов и запасных частей из фактуры"""
        orders_lines = self.driver.find_elements(By.CSS_SELECTOR, 'tr[role].even, tr[role].odd')
        return orders_lines

    @staticmethod
    def get_data_cells(order_line):
        """Получаем список ячеек данных из строки заказа"""
        data_cells = order_line.find_elements(By.CSS_SELECTOR, 'td')
        return data_cells

    @staticmethod
    def find_rejected_positions(data_cell):
        """
        передавая ячейку [1], проверяем наличие отказной метки
        :param data_cell: ячейка 1
        :return: text
        """
        print('\trun find_rejected_positions()')
        try:
            data_cell.find_element(By.CSS_SELECTOR, "td>img[title='Все позиции отклонены']")
            return True
        except NoSuchElementException:
            try:
                data_cell.find_element(By.CSS_SELECTOR,
                                       "td>img[title='Имеются частично  поставленные и отклоненные позиции']")
                return True
            except NoSuchElementException:
                print('\tFalse reject')
                return False

    @staticmethod
    def get_single_line_cell_text(data_cell):
        """
            получаем текст из ячейки с одной строкой.
            сумма поставки [12], комментарий [14],
            :param data_cell ячейка с текстом
            :return:str
            """
        try:
            text = data_cell.text
            return text
        except NoSuchElementException:
            return None

    @staticmethod
    def get_double_line_cell_text(data_cell):
        """
        получаем текст из ячейки с двумя строками.
        Дата заказа [3], дата поставки [4], дата фактуры[5]
        :param data_cell ячейка с текстом
        :return:str
        """
        try:
            date_from_cells = data_cell.find_element(By.CSS_SELECTOR, 'td>div>div').text
            return date_from_cells
        except (NoSuchElementException, AttributeError):
            return None

    @staticmethod
    def get_link_invoice(data_cell):
        """
        Получаем ссылку на фактуру
        :param data_cell: строка с заказом [5]
        :return: href
        """
        try:
            link = data_cell.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        except NoSuchElementException:
            return None
        return link

    @staticmethod
    def find_returns(data_cell):
        """
        Проверяем наличие возвратов
        :param data_cell: строка с заказом [0]
        :return: True
        """
        try:
            data_cell.find_element(By.CSS_SELECTOR, "img[title='Сторно']")
            return True
        except NoSuchElementException:
            return False

    @staticmethod
    def record_comment(comment):
        """
        Записываем комментарий об отказе в файл, если его там нет
        :return: True, если добавлено, False, если комментарий уже есть
        """
        print('\trun record_comment')
        with open('armtek.txt', 'r+', encoding='utf-8') as f:
            strings = f.readlines()
            strings = [line.strip() for line in strings]
            if comment.strip() in strings:
                print('\t\tвозврат уже зафиксирован')
                return False
            else:
                f.write(comment + "\n")
                print('\t\tзаписываем возврат')
            return True

    def change_organization(self):
        """
        меняем организацию, для которой собираем информацию
        """
        self.driver.find_element(By.ID, 'kunnrRgLink').click()
        self.driver.find_element(By.ID, 'kunnrRgMenu').click()

    @abstractmethod
    def check_delivery_date(self):
        """описываются условия выбора заказов по необходимы датам"""
        pass

    def get_data(self):
        """
        Собираем в единых список сумму и все комментарии предстоящих поставок
        добираемся по строкам до первой актуальной фактуры и return, дальше строки не просматриваются
        :return: список поставок
        """
        print('run get_data() from armtek')
        if self.comment:
            return self.comment
        else: return None
