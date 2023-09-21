# -*- coding: utf-8 -*-
import sys
import asyncio
import time
import mytoken, USD_RUB
import logging
import datetime
from aiogram import Bot, Dispatcher, executor, types
import WtoM,hashrateno, mineros, Hive, Hive, binance, armtek, monitoring_price_changes_minings_coins, timer
from aiogram.dispatcher import FSMContext, filters
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
    print(message.text.lower(), message)
    if message.text.lower() == 'хешрейт':
        await bot.send_message(message.from_user.id, Hive.get_hive_hashrate(), reply_markup=but)
    elif message.text.lower() == 'старт':
        await bot.send_message(message.from_user.id, "запуск...", reply_markup=but)
        print('старт')
        global course_change_observer
        course_change_observer = True
        await asyncio.gather(monitoring_of_armtek_delivery(message),monitoring_number_of_rigs(message, state),
                             monitoring_price_changes(message))
    elif message.text.lower() == 'стоп':
        course_change_observer = False
        print(course_change_observer)
    elif message.text.lower() == 'профит':
        for j in hashrateno.main_function():
            await bot.send_message(message.from_user.id, str(j).translate({ord(i):None for i in "[]'" }))
        for i in WtoM.whattomine():
            await bot.send_message(message.from_user.id, i)
    elif message.text.lower() == 'армтек':
        armtek_list = armtek.armtek()
        print('armtek_list', armtek_list)
        if not armtek_list:
            await bot.send_message(message.from_user.id, 'Пока поставка не сформирована')
        else:
            for i in armtek_list:
                await bot.send_message(message.from_user.id, i)
    elif message.text.lower() == 'курсы валют':
        for i in binance.get_cource_from_binance():
            await bot.send_message(message.from_user.id, i)
        for i in monitoring_price_changes_minings_coins.getting_coin_attrbutes():
            await  bot.send_message(message.from_user.id, text=i)
        await bot.send_message(message.from_user.id, text=USD_RUB.get_cource_usd_rub())


async def monitoring_number_of_rigs(message, state):
    while course_change_observer:
        await check_hive_work(message, state)
        print('monitoring_number_of_rigs run', course_change_observer)
        quantity_rigs_online = Hive.get_quantity_of_rig_online()
        if quantity_rigs_online < quantity_rigs:
            await asyncio.sleep(0.3)
            await bot.send_message(message.from_user.id, text='Hive rig offline, online rigs = ' + str(
                Hive.get_quantity_of_rig_online()))
            await asyncio.sleep(0.5)
            mineros.period = 30
            with open('log.txt', 'a') as log:
                log.write('Hive' + str(datetime.datetime.now()) + 'rig offline' +
                          str(Hive.get_quantity_of_rig_online()) + '\n')
        if quantity_rigs_online == quantity_rigs:
            mineros.period = 180
        await asyncio.sleep(mineros.period)


async def monitoring_price_changes(message):
    try:
        while course_change_observer:
            print('binance run', course_change_observer)
            for i in binance.get_cource_from_binance():
                print(i,(i[2][:-1]), float(i[2][:-1]))
                if float(i[2][:-1])>5 or float(i[2][:-1])<-5:
                    await bot.send_message(message.from_user.id, text="Изменение больше 5% "+str(i))
            gen=monitoring_price_changes_minings_coins.hashrate_no_get_coin_price()
            for i in gen :
                print(i)
                if i[3]>15 or i[3]<-15:
                    await bot.send_message(message.from_user.id, text="Изменение больше 15% " + str(i).
                                           translate({ord(i): None for i in '()'})+'% за 24 часа')
            u_r_get_cource = USD_RUB.get_cource_usd_rub()
            print(u_r_get_cource)
            if float(u_r_get_cource[1][:-1]) > 2 or float(u_r_get_cource[1][:-1]) < -2:
                await bot.send_message(message.from_user.id, text="Изменение больше 2% USD/RUB" + str(u_r_get_cource))
            await asyncio.sleep(3600*3)
    except:
        with open("log.txt", 'a') as log:
            log.write('monitoring_price_changes '+str(datetime.datetime.now())+' '+str(sys.exc_info())+'\n')


async def get_data_from_armtek_and_send_message(message):
    pause = 6000
    armtek_list = armtek.armtek()
    for i in armtek_list:
        await bot.send_message(message.from_user.id, i)
    await asyncio.sleep(pause)


async def monitoring_of_armtek_delivery(message):
    time_start_1 = '19:30'
    time_start_2 = '00:30'
    time_start_3 = '08:45'
    while True:
        if  await timer.timer(time_start_1 + ':00'):
            await get_data_from_armtek_and_send_message(message)
        elif await timer.timer(time_start_2 + ':00'):
            await get_data_from_armtek_and_send_message(message)
        elif await timer.timer(time_start_3 + ':00'):
            await get_data_from_armtek_and_send_message(message)
        else:
            print("armtek_monitor() False")


class GoogleKodAuthenticator(StatesGroup):
    """
    Класс для хранения состояний
    Для получения кода аутентификатора
    """
    waiting_kod = State()


async def need_send_kod(message: types.Message, state: FSMContext):
    """
 Для получения кода аутентификатора
  запускается, несмотря на фильтры, потому что функция запускается отдельным вызовом, минуя фильтры.
    """
    print('run kod')
    await message.answer('Нужен код')
    # устанавливаем  в состояние waiting kod
    await GoogleKodAuthenticator.waiting_kod.set()


# если убрать state=Google_kod.waiting_kod, то get_cod() не обработает state
@dp.message_handler(content_types=['text'],state=GoogleKodAuthenticator.waiting_kod)
async def get_kod_of_authenticator(message: types.Message, state: FSMContext):
    print('run get_kod_of_authenticator()')
    await state.update_data(G_kod=message.text)
    # получаем сохраненные данные из хранилища
    user_data = await state.get_data('G_kod')
    print('user_data', user_data)
    # получаем доступ к state как к словарю
    async with state.proxy() as data:
        Hive.hive_get_kod_of_authenticator(data['G_kod'])
    await state.finish()


async def check_hive_work(message, state: FSMContext):
    """
    Для получения кода аутентификатора(отключено)
    """
    pass
    # print('run check_hive_work()')
    # with open('hive_work.txt', 'r') as file:
    #    read= file.read()
    # if read == 'False':
    #     await need_send_kod(message, state)
try:
    executor.start_polling(dp)
except:
    with open('log.txt', 'a', encoding='utf-8') as log:
        log.write('start_polling ' + str(datetime.datetime.now()) + ' нет соединения ' + str(sys.exc_info()) + '\n')
    time.sleep(2)
    executor.start_polling(dp, skip_updates=True)


