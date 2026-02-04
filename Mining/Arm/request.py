# -*- coding: utf-8 -*-
import asyncio
import datetime
import logging
import sys
import main_armtek
import timer
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Mining import hashrateno
from Mining import mytoken


# создали хранилище памяти
storage = MemoryStorage()
logger = logging.getLogger(__name__)
bot = Bot(mytoken.tokenbot)
#  передали экземпляру класса диспетчера бота и хранилище
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(content_types=['text'])
async def send_message(message, state):
    but = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn2 = types.KeyboardButton('Старт')
    btn3 = types.KeyboardButton('Стоп')
    btn4 = types.KeyboardButton('профит')
    btn5 = types.KeyboardButton('Армтек')
    but.add(btn2, btn3, btn4, btn5)
    global course_change_observer
    course_change_observer = False
    print(message.text.lower(), message)
    if message.text.lower() == 'старт':
        await bot.send_message(message.from_user.id, "запуск...", reply_markup=but)
        print('course_change_observer =', course_change_observer)
        if not course_change_observer and counter() == 1:
            course_change_observer = True
            await monitoring_armtek_delivery(message, but)
        else:
            print('еще раз нажали "старт" ')
    elif message.text.lower() == 'стоп':
        course_change_observer = False
    elif message.text.lower() == 'профит':
        for j in hashrateno.main_function():
            await bot.send_message(message.from_user.id, str(j).translate({ord(i): None for i in "[]'"}))
    elif message.text.lower() == 'армтек':
        await get_data_from_armtek_and_send_message(message, but)


def message_counter():
    """ Счетчик нажатий "старт" """
    counter = 0

    def closure():
        nonlocal counter
        counter += 1
        return counter
    return closure


counter = message_counter()


async def get_data_from_armtek_and_send_message(message, but):
    armtek_list = main_armtek.main()
    print('armtek_list', armtek_list)
    if not armtek_list:
        await bot.send_message(message.from_user.id, 'Пока поставка не сформирована, отказов нет')
    else:
        counter = 0
        empty_str = 0
        for i in armtek_list:
            counter += 1
            if i is None and counter == len(armtek_list) and empty_str == 0:
                await bot.send_message(message.from_user.id, 'Пока поставка не сформирована, отказов нет',
                                       reply_markup=but)
            elif i is None:
                continue
            else:
                empty_str += 1
                if isinstance(i, list):
                    for k in i:
                        print('\t\t\t\t\tk= ', k)
                        await bot.send_message(message.from_user.id, k, reply_markup=but)
                else:
                    await bot.send_message(message.from_user.id, i, reply_markup=but)


async def monitoring_armtek_delivery(message, but):
    """
    отслеживание поставок по времени
    """
    print('run monitoring_of_armtek_delivery')
    time_start_1 = '20:00'
    time_start_2 = '23:53'
    time_start_3 = '08:00'
    time_start = [time_start_3, time_start_2, time_start_1]
    while True:
        await asyncio.sleep(60)
        for i in time_start:
            if await timer.timer(i + ':00'):
                await get_data_from_armtek_and_send_message(message, but)
        else:
            print("armtek_monitor() False")


try:
    executor.start_polling(dp, skip_updates=False)
except:
    with open('../log.txt', 'a', encoding='utf-8') as log:
        log.write('start_polling ' + str(datetime.datetime.now()) + ' нет соединения ' + str(sys.exc_info()) + '\n')


