# -*- coding: utf-8 -*-
import sys
import asyncio
import time
import mytoken, USD_RUB
import logging
import datetime
from aiogram import Bot, Dispatcher, executor, types
import What_to_mine,hashrateno, mineros, Hive, binance, armtek,\
    monitoring_price_changes_minings_coins, timer, monitoring_the_number_of_rings_rplant as rplant
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
quantity_rigs = 4

# создали хранилище памяти
storage = MemoryStorage()
logger = logging.getLogger(__name__)
bot=Bot(mytoken.tokenbot)
#  передали экземпляру класса диспетчера бота и хранилище
dp=Dispatcher(bot,storage=storage)


@dp.message_handler(content_types=['text'] )
async def send_message(message, state):
    but = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('хешрейт')
    btn2 = types.KeyboardButton('Старт')
    btn3 = types.KeyboardButton('Стоп')
    btn4 = types.KeyboardButton('профит')
    btn5 = types.KeyboardButton('Армтек')
    btn6 = types.KeyboardButton('курсы валют')
    but.add(btn1, btn2, btn3, btn4, btn5, btn6)
    global course_change_observer
    course_change_observer = False
    print(message.text.lower(), message)
    if message.text.lower() == 'хешрейт':
        hashrate = rplant.monitoring_of_mining()
        await bot.send_message(message.from_user.id, 'мгновенный хешрейт - '+ hashrate[1]
                                + '\n средний хешрейт - ' + hashrate[2], reply_markup=but)
    elif message.text.lower() == 'старт':
        await bot.send_message(message.from_user.id, "запуск...", reply_markup=but)
        print('старт')
        if not course_change_observer:
            course_change_observer = True
            await asyncio.gather(monitoring_price_changes(message), monitoring_number_of_rigs(message),
                             monitoring_of_armtek_delivery(message))
    elif message.text.lower() == 'стоп':
        course_change_observer = False
    elif message.text.lower() == 'профит':
        for j in hashrateno.main_function():
            await bot.send_message(message.from_user.id, str(j).translate({ord(i):None for i in "[]'" }))
        for i in What_to_mine.get_profit_of_coins():
            await bot.send_message(message.from_user.id, i)
    elif message.text.lower() == 'армтек':
       await get_data_from_armtek_and_send_message(message)
    elif message.text.lower() == 'курсы валют':
        for i in binance.get_cource_from_binance():
            await bot.send_message(message.from_user.id, i)
        for i in monitoring_price_changes_minings_coins.getting_coin_attrbutes():
            await  bot.send_message(message.from_user.id, text=i)
        await bot.send_message(message.from_user.id, text=USD_RUB.main())


async def get_message_about_rigs(message):
    driver = rplant.get_driver_selenium()
    driver.get(rplant.get_rplant_url())
    rplant.find_wallet(driver)
    table_of_hashrate = rplant.hashrate_of_rigs(driver)
    await bot.send_message(message.from_user.id, text=table_of_hashrate)


async def monitoring_number_of_rigs(message):
    while course_change_observer:
        # await check_hive_work(message, state)
        print('monitoring_number_of_rigs run', course_change_observer)
        await get_message_about_rigs(message)
        result_monitoring_number_of_rigs_rplant = rplant.monitoring_of_mining()
        quantity_rigs_online = result_monitoring_number_of_rigs_rplant[0]
        hashrate_of_rigs = result_monitoring_number_of_rigs_rplant[3]
        if quantity_rigs_online < quantity_rigs:
            await asyncio.sleep(0.3)
            await bot.send_message(message.from_user.id, text='Rig offline, online rigs = ' + str(
                                                                    quantity_rigs_online)+'\n' + hashrate_of_rigs )
            await asyncio.sleep(0.5)
            mineros.period = 30
            with open('log.txt', 'a') as log:
                log.write( str(datetime.datetime.now()) + 'rig offline' +
                          str(quantity_rigs_online) + '\n')
        elif quantity_rigs_online == quantity_rigs:
            mineros.period = 180
        await asyncio.sleep(mineros.period)


async def monitoring_price_changes(message):
    # try:
        while course_change_observer:
            print('binance run', course_change_observer)
            for i in binance.get_cource_from_binance():
                try:
                    print(i,(i[2][:-1]), float(i[2][:-1]))
                    if float(i[2][:-1])>5 or float(i[2][:-1])<-5:
                        await bot.send_message(message.from_user.id, text="Изменение больше 5% "+str(i))
                except:
                    continue
            for i in monitoring_price_changes_minings_coins.hashrateno_get_coin_price():
                print(i)
                if i[3] == 'N/':
                    await bot.send_message(message.from_user.id, text="По измененияем нет данных ")
                elif float(i[3])>15 or float(i[3])<-15:
                        await bot.send_message(message.from_user.id, text="Изменение больше 15% " + str(i).
                                               translate({ord(i): None for i in '()'})+'% за 24 часа')
            cource_rub_usd = USD_RUB.main()
            await bot.send_message(message.from_user.id, text=cource_rub_usd)
            print(cource_rub_usd)
            await asyncio.sleep(3600*3)
    # except:
    #     with open("log.txt", 'a') as log:
    #         log.write('monitoring_price_changes '+str(datetime.datetime.now())+' '+str(sys.exc_info())+'\n')


async def get_data_from_armtek_and_send_message(message):
    armtek_list = armtek.main()
    print('armtek_list', armtek_list)
    if not armtek_list:
        await bot.send_message(message.from_user.id, 'Пока поставка не сформирована, отказов нет')
    else:
        counter = 0
        empty_str = 0
        for i in armtek_list:
            counter += 1
            if i == '' and counter == len(armtek_list) and empty_str == 0:
                await bot.send_message(message.from_user.id, 'Пока поставка не сформирована, отказов нет')
            elif i == '':
                continue
            else:
                empty_str += 1
                await bot.send_message(message.from_user.id, i)


async def monitoring_of_armtek_delivery(message):

    time_start_1 = '20:40'
    time_start_2 = '23:30'
    time_start_3 = '08:45'
    time_start = [time_start_3, time_start_2, time_start_1]
    while True:
        # await asyncio.sleep(pause)
        for i in time_start:
            if await timer.timer(i + ':00'):
                await get_data_from_armtek_and_send_message(message)
        else:
            print("armtek_monitor() False")


# class GoogleKodAuthenticator(StatesGroup):
#     """
#     Класс для хранения состояний
#     Для получения кода аутентификатора
#     """
#     waiting_kod = State()
#

# async def need_send_kod(message: types.Message, state: FSMContext):
#     """
#  Для получения кода аутентификатора
#   запускается, несмотря на фильтры, потому что функция запускается отдельным вызовом, минуя фильтры.
#     """
#     print('run kod')
#     await message.answer('Нужен код')
#     # устанавливаем  в состояние waiting kod
#     await GoogleKodAuthenticator.waiting_kod.set()


# # если убрать state=Google_kod.waiting_kod, то get_cod() не обработает state
# @dp.message_handler(content_types=['text'],state=GoogleKodAuthenticator.waiting_kod)
# async def get_kod_of_authenticator(message: types.Message, state: FSMContext):
#     print('run get_kod_of_authenticator()')
#     await state.update_data(G_kod=message.text)
#     # получаем сохраненные данные из хранилища
#     user_data = await state.get_data('G_kod')
#     print('user_data', user_data)
#     # получаем доступ к state как к словарю
#     async with state.proxy() as data:
#         Hive.hive_get_kod_of_authenticator(data['G_kod'])
#     await state.finish()
#     await bot.send_message(message.from_user.id,text=Hive.get_hive_hashrate())


# async def check_hive_work(message, state: FSMContext):
#     """
#     Для получения кода аутентификатора()
#     """
#     print('run check_hive_work()')
#     with open('hive_work.txt', 'r') as file:
#        read= file.read()
#     if read == 'False':
#         await need_send_kod(message, state)
try:
    executor.start_polling(dp)
except:
    with open('log.txt', 'a', encoding='utf-8') as log:
        log.write('start_polling ' + str(datetime.datetime.now()) + ' нет соединения ' + str(sys.exc_info()) + '\n')
    time.sleep(2)
    executor.start_polling(dp, skip_updates=True)


