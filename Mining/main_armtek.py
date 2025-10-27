"""Главный файл армтек"""

import traceback
import datetime
import time
import armtek_morning_evening as ame


def select_of_class():
    """
    Выбираем какую функцию вызывать в зависимости от времени суток
    :return: None
    """
    time_now = datetime.datetime.now().time()
    time_object_12_00_00, time_object_00_00_00, time_object_05_00_00, time_object_23_59_59 = get_times_objects()
    try:
        if time_object_05_00_00 < time_now < time_object_12_00_00:
            return ame.MorningRequest()
        else:
            return ame.EveningRequest()
    except TypeError:
        traceback.print_exc()


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


def record_reject(request):
    """
    записываем отказные позиции в файл или проверяем наличие записи
    :param request:
    :return: comment
    """
    print('run record_reject')
    if request.reject:
        print('\trejected_positions = ', request.comment)
        if request.record_comment(request.comment):
            comment = "Отказ, " + "Заказ от " + request.order_date + ' ' + request.comment
            return comment
        else:
            return None
    return None


def record_returns(request):
    """
    проверяя соответствущую ячейку, определяем проведен ли возврат или нет и возвращаем соответствующую запись
    :param request:
    :return: comment
    """
    if request.returns:
        if request.invoice_date == datetime.date.today():
            comment = 'Возврат ' + request.comment + ' на сумму ' + request.delivery_amount + ' проведен'
            return comment
        elif not request.invoice_date:
            comment = 'Возврат ' + request.comment + ' на сумму ' + request.delivery_amount + ' не проведен'
            print('\t', 'comment = ', comment)
            return comment
        return None
    else:
        return None


def fetch_web_data(request):
    """request """
    print('run fetch_web_data')
    delivery_list = []
    request.get_right_page()
    request.wait_for_page_load()
    request.set_cookies()
    '''повторный вызов нужен для того, чтобы применить куки'''
    request.get_right_page()
    if not request.check_right_page():
        request.log_in_armtek()
        time.sleep(3)
        if not request.check_right_page():
            print('\tНе вошли в Армтек')
            return ['Не вошли в Армтек']
    request.write_of_cookies_in_file()
    request.set_date_of_orders()
    time.sleep(2)
    for order_line in request.get_strings():
        print("Новая строка")
        request.data_cells = request.get_data_cells(order_line)
        request.reject = request.find_rejected_positions(request.data_cells[1])
        print('\trequest.reject = ', request.reject)
        request.comment = request.get_single_line_cell_text(request.data_cells[14])
        print('\trequest.comment = ', request.comment)
        request.delivery_amount = request.get_single_line_cell_text(request.data_cells[12])
        print('\trequest.delivery_amount = ', request.delivery_amount)
        request.order_date = request.get_double_line_cell_text(request.data_cells[3])
        print('\trequest.order_date = ', request.order_date)
        request.delivery_date = request.get_double_line_cell_text(request.data_cells[4])
        print('\trequest.delivery_date = ', request.delivery_date)
        request.invoice_date = request.get_double_line_cell_text(request.data_cells[5])
        print('\trequest.invoice_date = ', request.invoice_date)
        request.invoice_link = request.get_link_invoice(request.data_cells[5])
        print('\trequest.invoice_link = ', request.invoice_link)
        request.returns = request.find_returns(request.data_cells[0])
        print('\trequest.returns = ', request.returns)
        comment_reject = record_reject(request)
        comment_returns = record_returns(request)
        delivery_list.append(comment_reject)
        delivery_list.append(comment_returns)
        print('\trecord_returns(request) = ', comment_returns)
        if request.check_delivery_date() and not comment_reject and not comment_returns:
            delivery = request.get_data()
            delivery_list.append(delivery)
            print('\t\t\trequest =', isinstance(request, ame.MorningRequest))
            if isinstance(request, ame.MorningRequest):
                break  # останавливаем цикл, когда получаем фактуру в утреннем запросе
        else:
            continue
    if not delivery_list:
        delivery_list.append('Поставки нет')
    return delivery_list


def main():
    """
    request главная функция
    """
    request = select_of_class()
    try:
        time.sleep(3)
        first_spare_parts = fetch_web_data(request)
        request.change_organization()
        second_spare_parts = fetch_web_data(request)
        request.driver.quit()
        print('\t\t\tmy_spare_parts = ', first_spare_parts+second_spare_parts)
        return first_spare_parts + second_spare_parts
    except:
        request.driver.quit()
        traceback.print_exc()


if __name__ == '__main__':
    main()
