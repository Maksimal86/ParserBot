# -*- coding: utf-8 -*-
import mytoken, asyncio, datetime
from aiogram.types import InputFile
from aiogram import Bot, Dispatcher, executor, types
import eth_btc, \
        monitoring_of_rigs_wooly_pooly as pool, USD_RUB,mineros, monitoring_price_changes_minings_coins
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()
bot = Bot(mytoken.tokenbot_kurs)
dp = Dispatcher(bot, storage=storage)
quantity_rigs = 4
course_change_observer = False


@dp.message_handler(content_types=['text'])
async def send_message(message):
    but = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('старт')
    btn2 = types.KeyboardButton('Стоп')
    btn3 = types.KeyboardButton('Курсы')
    but.add(btn1, btn2, btn3)
    global course_change_observer
    if message.text.lower() == 'старт':
        print('course_change_observer =', course_change_observer)
        if counter() == 1:
            await bot.send_message(message.from_user.id, "запуск...", reply_markup=but)
            course_change_observer = True
            await asyncio.gather(monitoring_price_changes(message),monitoring_number_of_rigs(message))
        elif counter() >= 1 and course_change_observer:
            await bot.send_message(message.from_user.id, "старт уже был нажат")
    elif message.text.lower() == 'стоп':
        course_change_observer = False
    elif message.text.lower() == 'курсы':
        for i in eth_btc.get_cource():
            await bot.send_message(message.from_user.id, i)
        for i in monitoring_price_changes_minings_coins.getting_coin_attributes():
            await bot.send_message(message.from_user.id, text=i[0] + i[1] + '  ' + i[2] + ' за 1 час, ' + i[3] + '%  за 24 часа')
        await bot.send_message(message.from_user.id, USD_RUB.main())


def message_counter():
    '''Счетчик нажатий "старт"'''
    counter = 0
    def closure():
        nonlocal counter
        counter += 1
        print('counter=', counter)
        return counter
    return closure
counter = message_counter()


async def monitoring_price_changes(message):
    '''Получаем информацию о ценах и их изменениях и отправляем соответствующее сообщение'''
    while course_change_observer:
        print('while')
        list_of_coins = '\n'.join(eth_btc.get_cource())
        await bot.send_message(message.from_user.id, text=list_of_coins)
        for i in monitoring_price_changes_minings_coins.getting_coin_attributes():
            if i[3] == 'N/':
                await bot.send_message(message.from_user.id, text="По изменениям нет данных ")
            elif float(i[3]) > 15 or float(i[3]) < -15:
                await bot.send_message(message.from_user.id, text=i[0] + i[1] + " Изменение больше 15%  " + i[2].
                                       translate({ord(i): None for i in '()'}) + ' за 1 час, ' + i[3] + '%  за 24 часа')
        cource_rub_usd = USD_RUB.main()
        await bot.send_message(message.from_user.id, text=cource_rub_usd)
        print(cource_rub_usd)
        await asyncio.sleep(3600)


async def send_message_about_rigs(message):
    '''Готовим и отправляем сообщение в нужном формате'''
    result_monitoring = pool.main()
    screenshort = InputFile('graphic_HR.png')
    list_of_data =result_monitoring [0]
    quantity_rigs_online = result_monitoring[1]
    remove_chars = "[]',"
    translation_table = str.maketrans("", "", remove_chars)
    str_message = str(list_of_data).translate(translation_table)
    await bot.send_message(message.from_user.id, text=str_message +' \n Норма \n  1080 = 70Mh/s \n'
                                                                          '5600 10 = 200Mh/s \n'
                                                                          '5600 12 = 240Мh/s \n '
                                                                          '5700 = 143Mh/s'
                                                                   
                           '\n Количество ригов = ' +str(quantity_rigs_online))
    await bot.send_photo(message.from_user.id, screenshort)
    return quantity_rigs_online


async def monitoring_number_of_rigs(message):
    while course_change_observer:
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


try:
    executor.start_polling(dp)
except:
    # await bot.send_message(message.from_user.id, "запуск после ошибки...", reply_markup=but)
    course_change_observer = True
    # await monitoring_price_changes(message)
    executor.start_polling(dp)