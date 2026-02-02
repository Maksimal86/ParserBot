"""класс MorningRequest"""

import datetime
import sys
import time
import armtek
from selenium.common.exceptions import NoSuchElementException
from datetime import date, timedelta


class MorningRequest(armtek.Basic):
    """
        класс определят сбор информации в утреннее время
    """

    def __init__(self):
        super().__init__()
        self.invoice_link = None
        self.invoice_date = None

    def check_delivery_date(self):
        """описываются условия выбора заказов по необходимой дате,
        если дата фактуры сегодняшняя
        :return: True
        """                                                           
        print('\trun check_delivery_date morning', (date.today() - datetime.timedelta(days=0)).strftime("%d.%m.%Y"))
        try:
            if (date.today() - timedelta(days=0)).strftime("%d.%m.%Y") == self.invoice_date:
                print('\t\tДата фактуры - True')
                return True
            else:
                print('\t\tДата фактуры - False')
        except NoSuchElementException:
            print('\t\t', sys.exc_info())
            return False

    def get_invoice(self, link):
        """
        Заходим на страницу заказа
        """
        self.driver.get(link)
        time.sleep(4)

    @staticmethod
    def get_spare_part_by_invoice(spare_parts_cells):
        """
        получаем наименование запчасти в фактуре
        :param spare_parts_cells: ячейка с наименованием запчасти
        :return: str запчасть
        """
        time.sleep(1)
        spare_part = MorningRequest.get_single_line_cell_text(spare_parts_cells)
        print('\t\tspare_part = ', spare_part)
        return spare_part

    @staticmethod
    def get_comment_from_invoice(comment_cells):
        """
        Получаем комментарий из строки заказа
        :param comment_cells: список ячеек из строки заказа
        """
        comment = MorningRequest.get_single_line_cell_text(comment_cells)
        return comment

    def get_data(self):
        """
        Собираем в единых список сумму и все комментарии предстоящих поставок
        добираемся по строкам до первой актуальной фактуры и return, дальше строки не просматриваются
        :return: список поставок
        """
        print('\trun get_data')
        spare_parts_list = []
        self.driver.get(self.invoice_link)
        time.sleep(2)
        spare_parts_strings = self.get_strings()
        for string in spare_parts_strings:
            data_cells_spare_parts = self.get_data_cells(string)
            comment = self.get_single_line_cell_text(data_cells_spare_parts[10])
            spare_part = self.get_single_line_cell_text(data_cells_spare_parts[4])
            spare_parts_list.append(comment + ' Запчасти:\n' + spare_part)
            print('\t\tspare_parts_list = ', spare_parts_list)
        if spare_parts_list:
            return spare_parts_list
        else:
            print('\tstr99,нет поставки')
            return None


class EveningRequest(armtek.Basic):
    """
    Класс определяет сбор информации в вечернее время
    """

    def __init__(self):
        super().__init__()
        self.comment = None
        self.invoice_date = None
        self.delivery_date = None

    def check_delivery_date(self):
        """
        описываются условия выбора заказов по необходимы датам
        если дата поставки вчерашняя и даты фактуры нет или она или поставка сегодняшняя, а фактуры нет
        :return: True
        """
        print("run check_delivery_date")
        try:
            if (date.today() - datetime.timedelta(days=0)).strftime("%d.%m.%Y") == \
                    self.delivery_date and self.invoice_date is None or \
                    date.today().strftime("%d.%m.%Y") == self.delivery_date and self.invoice_date is None:
                print('\tcheck_delivery_date True')
                return True
            else:
                print("\tcheck_delivery_date False")
                return False
        except NoSuchElementException:
            print(sys.exc_info())
            return False

    def get_data(self):
        """
        Собираем в список комментарии поставок, прошедших проверку check_delivery_date()
        """
        list_comment = [self.comment]
        return list_comment
