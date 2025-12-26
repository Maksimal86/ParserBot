# -*- coding: utf-8 -*-
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InputFile
import USD_RUB
import asyncio
import datetime
import eth_btc
import mineros
import monitoring_of_rigs_wooly_pooly as pool
import monitoring_price_changes_minings_coins
import mytoken
import requests.exceptions

storage = MemoryStorage()
bot = Bot(mytoken.tokenbot_kurs)
dp = Dispatcher(bot, storage=storage)
quantity_rigs = 5
course_change_observer = False


@dp.message_handler(content_types=['text'])
async def send_message(message):
    """
    Принимает сообщения и запускает соответствующие функции
    """
    but = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Старт майнинг')
    btn2 = types.KeyboardButton('Стоп')
    btn3 = types.KeyboardButton('Курсы')
    btn4 = types.KeyboardButton('Старт курсы')
    but.add(btn1, btn2, btn3, btn4)
    global course_change_observer

    course_change_observer = True
    if message.text == 'x':
        await bot.send_message(message.from_user.id, "Кнопки", reply_markup=but)
    elif message.text.lower() == 'старт майнинг':
        course_change_observer = True
        if counter() < 2:
            await bot.send_message(message.from_user.id, "запуск отслеживания майнинга...", reply_markup=but)
            await monitoring_number_of_rigs(message)
        elif counter() >= 1 and course_change_observer:
            await bot.send_message(message.from_user.id, "старт уже был нажат")
    elif message.text.lower() == 'стоп':
        course_change_observer = False
        reset_counter()
    elif message.text.lower() == 'старт курсы':
        await bot.send_message(message.from_user.id, 'запуск отслеживания курсов валют...', reply_markup=but)
        await monitoring_price_changes(message)
    elif message.text.lower() == 'курсы':
        for i in eth_btc.get_cource():
            await bot.send_message(message.from_user.id, i)
        for i in monitoring_price_changes_minings_coins.getting_coin_attributes():
            await bot.send_message(message.from_user.id,
                                   text=i[0] +' '+ i[1] + '  ' + i[2][:-1])
        await bot.send_message(message.from_user.id, USD_RUB.main())
    print('course_change_observer =', course_change_observer)
    print('chatid =', message.chat.id)


def message_counter():
    """Счетчик нажатий "старт\""""
    click_counter = 0

    def click_counter_start():
        """
        счетчик
        """
        nonlocal click_counter
        click_counter += 1
        print('counter=', click_counter)
        return click_counter

    def reset():
        """сброс счетчика"""
        nonlocal click_counter
        click_counter = 0

    return click_counter_start, reset


counter, reset_counter = message_counter()


async def monitoring_price_changes(message):
    """Получаем информацию о ценах и их изменениях и отправляем соответствующее сообщение"""
    while True:
        print('while')
        try:
            list_of_coins = '\n'.join(eth_btc.get_cource())
        except (requests.exceptions.ConnectionError, ConnectionResetError):
            await bot.send_message(message.from_user.id, text="Нет данных по изменениям: https://www.rbc.ru/ не доступен")
        await bot.send_message(message.from_user.id, text=list_of_coins)
        try:
            for i in monitoring_price_changes_minings_coins.getting_coin_attributes():
                try:
                    print('i[2][:-3] = ', i[2][:-3])
                    if i[2] == 'N/':
                        await bot.send_message(message.from_user.id, text="По изменениям нет данных ")
                    elif float(i[2][:-3]) > 15 or float(i[2][:-3]) < -15:
                        await bot.send_message(message.from_user.id, text=i[0] + i[1] + " Изменение больше 15%  " + i[2][:-2].
                                               translate({ord(i): None for i in '()'}))
                except ValueError:
                    await bot.send_message(message.from_user.id, text=i[0]+" Нет данных ")
        except (requests.exceptions.ConnectionError, ConnectionResetError):
            await bot.send_message(message.from_user.id, text="Нет данных по изменениям: www.hashrate.no не доступен")
            print("www.hashrate.no не доступен")
        try:
            cource_rub_usd = USD_RUB.main()
            await bot.send_message(message.from_user.id, text=cource_rub_usd)
            print(cource_rub_usd)
        except (requests.exceptions.ConnectionError, ConnectionResetError):
            await bot.send_message(message.from_user.id, text="Нет данных по курсу USD: https://cbr.ru/ не доступен ")
        await asyncio.sleep(3600)


async def send_message_about_rigs(message):
    """Готовим и отправляем сообщение в нужном формате"""
    result_monitoring = pool.main()
    screenshort = InputFile('graphic_HR.png')
    list_of_data = result_monitoring[0]
    quantity_rigs_online = result_monitoring[1]
    remove_chars = "[]',"
    translation_table = str.maketrans("", "", remove_chars)
    str_message = str(list_of_data).translate(translation_table)
    await bot.send_message(message.from_user.id, text=str_message + ' \n Норма \n  1080 = 70Mh/s \n'
                                                                    '5600 10 = 200Mh/s \n'
                                                                    '5600 12 = 240Мh/s \n '
                                                                    '5700 = 143Mh/s'
                                                                    '\n Количество ригов = ' + str(
                                                                        quantity_rigs_online))
    await bot.send_photo(message.from_user.id, screenshort)
    return quantity_rigs_online


async def monitoring_number_of_rigs(message):
    """
    отслеживает количество ригов онлайн
    """
    print('run monitoring_number_of_rigs')
    while course_change_observer:
        print('while', course_change_observer)
        task = asyncio.create_task(send_message_about_rigs(message))
        await task
        quantity_rigs_online = task.result()
        print('monitoring_number_of_rigs run', course_change_observer)
        if int(quantity_rigs_online) < quantity_rigs:
            print('quantity_rigs_online = ', quantity_rigs_online)
            await bot.send_message(message.from_user.id, text='Rig offline, online rigs = ' + str(
                quantity_rigs_online))
            mineros.period = 30
            with open('log.txt', 'a') as log:
                log.write(str(datetime.datetime.now()) + 'rig offline' +
                          str(quantity_rigs_online) + '\n')
        elif quantity_rigs_online == quantity_rigs:
            mineros.period = 3600
        await asyncio.sleep(mineros.period)
while True:
    try:
        executor.start_polling(dp)
    except Exception as e:
        bot.send_message(1333130301, text=f'ошибка {e}, перезапуск бота')
        continue
