# -*- coding: utf-8 -*-
import mytoken, asyncio, datetime
from aiogram import Bot, Dispatcher, executor, types
import eth_btc, \
        monitoring_the_number_of_rings_rplant as rplant, USD_RUB,mineros, monitoring_price_changes_minings_coins

from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(mytoken.tokenbot_kurs)
dp = Dispatcher(bot, storage=storage)
quantity_rigs = 4

@dp.message_handler(content_types=['text'])

async def send_message(message, state):
    but = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('старт')
    btn2 = types.KeyboardButton('Стоп')
    btn3 = types.KeyboardButton('Курсы')
    but.add(btn1, btn2, btn3)
    global course_change_observer
    course_change_observer = False
    if message.text.lower() == 'старт':
        await bot.send_message(message.from_user.id, "запуск...", reply_markup=but)
        course_change_observer = True
        await asyncio.gather(monitoring_price_changes(message), monitoring_number_of_rigs(message))
    elif message.text.lower() == 'стоп':
        course_change_observer = False
    elif message.text.lower() == 'курсы':
        for i in eth_btc.get_cource():
            await bot.send_message(message.from_user.id, i)
        for i in monitoring_price_changes_minings_coins.getting_coin_attributes():
            await bot.send_message(message.from_user.id, text=i[0] + i[1] + i[2] + ' за 1 час, ' + i[3] + '%  за 24 часа')
        await bot.send_message(message.from_user.id, USD_RUB.main())


async def monitoring_price_changes(message):
    while course_change_observer:
        print('while')
        await get_message_about_rigs(message)
        for i in eth_btc.get_cource():
            await bot.send_message(message.from_user.id, text=str(i))
        for i in monitoring_price_changes_minings_coins.getting_coin_attributes():
            if i[3] == 'N/':
                await bot.send_message(message.from_user.id, text="По изменениям нет данных ")
            elif float(i[3]) > 15 or float(i[3]) < -15:
                await bot.send_message(message.from_user.id, text=i[0] + i[1] + " Изменение больше 15%  " + i[2].
                                       translate({ord(i): None for i in '()'}) + ' за 1 час, ' + i[3] + '%  за 24 часа')
        cource_rub_usd = USD_RUB.main()
        await bot.send_message(message.from_user.id, text=cource_rub_usd)
        print(cource_rub_usd)
        await asyncio.sleep(600 * 3)


async def get_message_about_rigs(message):
    driver = rplant.get_driver_selenium()
    driver.get(rplant.get_rplant_url())
    rplant.find_wallet(driver)
    table_of_hashrate = rplant.hashrate_of_rigs(driver)
    await bot.send_message(message.from_user.id, text=table_of_hashrate + 'Норма \n 5600/10 = 200Мh/s \n'
                                                                          '5600/12 = 240Mh/s \n'
                                                                          '5700 = 143Mh/s \n '
                                                                          '1080 = 70Mh/s')

async def monitoring_number_of_rigs(message):
    while course_change_observer:
        # await check_hive_work(message, state)
        print('monitoring_number_of_rigs run', course_change_observer)
        result_monitoring_number_of_rigs_rplant = rplant.monitoring_of_mining()
        quantity_rigs_online = result_monitoring_number_of_rigs_rplant[0]
        hashrate_of_rigs = result_monitoring_number_of_rigs_rplant[3]
        if quantity_rigs_online < quantity_rigs:
            await asyncio.sleep(0.3)
            await bot.send_message(message.from_user.id, text='Rig offline, online rigs = ' + str(
                quantity_rigs_online) + '\n' + hashrate_of_rigs)
            await asyncio.sleep(0.5)
            mineros.period = 30
            with open('log.txt', 'a') as log:
                log.write(str(datetime.datetime.now()) + 'rig offline' +
                          str(quantity_rigs_online) + '\n')
        elif quantity_rigs_online == quantity_rigs:
            mineros.period = 180
        await asyncio.sleep(mineros.period)


try:
    executor.start_polling(dp)
except:
    # await bot.send_message(message.from_user.id, "запуск после ошибки...", reply_markup=but)
    course_change_observer = True
    # await monitoring_price_changes(message)
    executor.start_polling(dp)