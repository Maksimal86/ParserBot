# -*- coding: utf-8 -*-
import sys
import asyncio
import time
import mytoken, USD_RUB
import logging
import datetime
from aiogram import Bot, Dispatcher, executor, types
import WtoM,hashrateno2, mineros, Hive, binance, armtek, delta_price_minings_coins, timer
from aiogram.dispatcher import FSMContext, filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
righive=4
#rigmineros=2
storage = MemoryStorage() #создали хранилище памяти
logger = logging.getLogger(__name__)
bot=Bot(mytoken.tokenbot)
dp=Dispatcher(bot,storage=storage)#  передали экзепляру класса диспетчера бота и хранилище

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
        #await bot.send_message(message.from_user.id, mineros.hashrate(), reply_markup=but)
        await bot.send_message(message.from_user.id, Hive.hive_hashrate(), reply_markup=but)

    elif message.text.lower() == 'старт': #запуск Wdog
        await bot.send_message(message.from_user.id, "запуск...", reply_markup=but)
        print('старт')
        global monitor
        monitor = 1
        await asyncio.gather(armtek_momitor(message),monitor_hashrate(message, state),delta_price(message))  # одновременный запуск асинхронных функций
    elif message.text.lower() == 'стоп':# остановка Wdog
        monitor = 0
        print(monitor)
    elif message.text.lower() == 'профит': # Парсинг hashrate.no и what to mine с выводом соответствующих данных о доходности
        if hashrateno2.error == 0:
            print(hashrateno2.error)
            await bot.send_message(message.from_user.id, 'Нет соединения с сайтом')
        elif type(WtoM.whattomine()) ==  str:
            await bot.send_message(message.from_user.id, 'Нет соединения с сайтом')
        else:
            for j in hashrateno2.hasrateno():
                await bot.send_message(message.from_user.id, str(j).translate({ord(i):None for i in "[]'" }))
            for i in WtoM.whattomine():
                await bot.send_message(message.from_user.id, i)
    elif message.text.lower() == 'армтек':
        armtek_list = armtek.armtek()[:]
        print('armtek_list', armtek_list)
        if armtek_list == []:
            await bot.send_message(message.from_user.id, 'Пока поставка не сформирована')
        else:
            for i in armtek_list:
                await bot.send_message(message.from_user.id, i)
    elif message.text.lower() == 'курсы валют':
        for i in binance.bin():
            await bot.send_message(message.from_user.id, i)
        for i in delta_price_minings_coins.hashrate_no_get_coin_price():
            await  bot.send_message(message.from_user.id, text=i)
        await bot.send_message(message.from_user.id, text=USD_RUB.get_course())

  #  else:
  #      await bot.send_message(message.chat.id, 'Неизвестная команда')


# Наблюдение за количеcтвом ригов онлайн
async def monitor_hashrate(message, state):
    while monitor:
        await check_hive_work(message, state)
        print('monitor hashrate run', monitor)
        quantity_rigs_online = Hive.save_onlinehive()
        if quantity_rigs_online < righive:
            await asyncio.sleep(0.3)
            await bot.send_message(message.from_user.id, text='Hive rig offline, online rigs = ' + str(
                Hive.save_onlinehive()))
            await asyncio.sleep(0.5)
            mineros.period=30
            with open('log.txt', 'a') as log:
                log.write('Hive' + str(datetime.datetime.now()) + 'rig offline' + str(Hive.save_onlinehive()) + '\n')
        if quantity_rigs_online == righive: mineros.period=180
        await asyncio.sleep(mineros.period)

async def delta_price(message):
    try:
        while monitor:
            print('binance run', monitor)
            for i in binance.bin():
                print(i,(i[2][:-1]), float(i[2][:-1]))
                if float(i[2][:-1])>5 or float(i[2][:-1])<-5:
                    await bot.send_message(message.from_user.id, text="Изменение больше 5% "+str(i))
            gen=delta_price_minings_coins.hashrate_no_get_coin_price()
            for i in gen :
                print(i)
                if i[3]>15 or i[3]<-15:
                    await bot.send_message(message.from_user.id, text="Изменение больше 15% "+str(i).translate({ord(i): None for i in '()'})+'% за 24 часа')

            u_r_get_cource = USD_RUB.get_course()
            print(u_r_get_cource)
            if float(u_r_get_cource[1][:-1]) > 5 or float(u_r_get_cource[1][:-1]) < -5:
                await bot.send_message(message.from_user.id, text="Изменение больше 5% USD/RUB" + str(u_r_get_cource))
            await asyncio.sleep(3600)
    except:
        with open("log.txt", 'a') as log:
            log.write('delta_price '+str(datetime.datetime.now())+' '+str(sys.exc_info())+'\n')
async def armtek_momitor(message):
    time1='23:00'
    time2='01:30'
    time3='08:45'
    while True:
        if  await timer.timer(time1+ ':00') :
            armtek_list = armtek.armtek()[:]
            if armtek_list == []:
                await bot.send_message(message.from_user.id, 'Пока поставка не сформирована')
            else:
                for i in armtek_list:
                    await bot.send_message(message.from_user.id, i)
            await asyncio.sleep(600)
        elif await timer.timer(time2+ ':00'):
            armtek_list = armtek.armtek()[:]
            if armtek_list == []:
                await bot.send_message(message.from_user.id, 'Пока поставка не сформирована')
            else:
                for i in armtek_list:
                    await bot.send_message(message.from_user.id, i)
            await asyncio.sleep(600)
        elif await timer.timer(time3+ ':00'):
            armtek_list = armtek.armtek()[:]
            if armtek_list == []:
                await bot.send_message(message.from_user.id, 'Пока поставка Армтек не сформирована')
            else:
                for i in armtek_list:
                    await bot.send_message(message.from_user.id, i)
            await asyncio.sleep(600)
        else:
            print("armtek_monitor() False")
class Google_kod(StatesGroup): # создали класс для хранения состояний
    waiting_kod = State() # создали экземпляр класса состояния ожидания кода


async def need_send_kod(message: types.Message, state: FSMContext):
    print('run kod') # запускается, не смотря на фильтры, потому что функция запускается отдельным вызовом, минуя фильтры.
    await message.answer('Нужен код')
    await Google_kod.waiting_kod.set() # установливаем  в состояние wating kod

@dp.message_handler(content_types=['text'],state=Google_kod.waiting_kod)# если убрать state=Google_kod.waiting_kod, то get_cod() не обработает state
async def get_kod(message: types.Message, state: FSMContext):
    print('run get_kod()')
    await state.update_data(G_kod=message.text)
    user_data = await state.get_data('G_kod')# получаем сохраненные данные из хранилища
    #if len(user_data['waiting_kod']) == 6:
    print('user_data', user_data)
    async with state.proxy() as data: # получаем доступ к state как к словарю
        Hive.hive_get_kod(data['G_kod'])  #Hive.hive_get_kod(user_data['waiting_kod'])
    await state.finish()
async def check_hive_work(message, state: FSMContext):
    print('run check_hive_work()')
    with open('hive_work.txt', 'r') as file:
       read= file.read()
    if read == 'False':
        await need_send_kod(message, state)


try:
    executor.start_polling(dp)#(timeout=5, long_polling_timeout = 5)#(none_stop=True, interval=0)
except:
    with open('log.txt', 'a', encoding='utf-8') as log:
        log.write('start_polling ' + str(datetime.datetime.now()) + ' нет соединения ' + str(sys.exc_info()) + '\n')
    time.sleep(2)
    executor.start_polling(dp, skip_updates=True)#(timeout=5, long_polling_timeout=5)


