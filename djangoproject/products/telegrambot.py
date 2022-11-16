import telebot
from telebot import types
import asyncio
from asgiref.sync import sync_to_async
from telebot.async_telebot import AsyncTeleBot
from loguru import logger
import time, math
import sys
from pathlib import Path
django_path = str(Path(__file__).resolve().        parent.parent)
sys.path.insert(0, django_path)
from dborm import get_products_count, get_products_id, get_product_name, get_product_description, get_product_price, get_product_image



logger.add('logs/bot.log', format='{time} {level} {message}')

token = '5669662526:AAF5IKDO18_A293S-hEgqPsSdv86HjC5JGM'
bot = AsyncTeleBot(token)


@bot.message_handler(commands=['start', 'help'])
@logger.catch
async def send_welcome(message):
    logger.info(f'{str(message.chat.id)} | start bot')

    btn1 = types.InlineKeyboardButton('Products', callback_data='products')
    markup = types.InlineKeyboardMarkup([[btn1]])

    await bot.send_message(message.chat.id, f'Hello {message.from_user.first_name}', reply_markup = markup)

@logger.catch
async def gen_product_button(page=int):
    callback_page = str(page)
    products_id = await get_products_id()
    products_count = await get_products_count()
    page_count = math.ceil(products_count / 10)
    page = (page - 1) * 10

    if page / 10 == page_count: index = products_count
    else: index = page + 10
    products_id = products_id[page:index]

    products = []
    for i in range(await sync_to_async(len)(products_id)):
        product_name = await get_product_name(products_id[i])
        products.append([types.InlineKeyboardButton(text=str(product_name), callback_data=f'id {products_id[i]} p {callback_page}')])
    return products

@logger.catch
async def gen_page_button(page=int):
    pages = []
    page_count = math.ceil(await get_products_count() / 10)

    btn1 = types.InlineKeyboardButton(text='<<', callback_data='page 1')
    btn2 = types.InlineKeyboardButton(text=f'>>', callback_data='page ' + str(page_count))

    page_count_r = page_count - page
    page_count_l = page_count - page_count_r - 1

    if page_count >= 5:
        if page_count_l > 2 and page_count_r > 2: page_count_l = 2
        else: 
            if page_count_l > page_count_r: page_count_l = 5 - page_count_r - 1
    else: 
        if page_count_l > page_count_r: page_count_l = page_count - page_count_r - 1

    page_index = page - page_count_l
    if page_count >= 5: for_count = 5
    else: for_count = page_count
    int_list = ['0̲', '1̲', '2̲', '3̲', '4̲', '5̲', '6̲', '7̲', '8̲', '9̲']

    pages.append(btn1)
    for i in range(for_count):
        text = str(page_index + i)
        if int(text) == page:
            for x in range(10):
                text.replace(text, int_list[x])

        pages.append(types.InlineKeyboardButton(text=text, callback_data='page ' + str(page_index + i)))
    pages.append(btn2)

    return pages

@bot.message_handler(content_types=['text'])
@logger.catch
async def bot_func(message):
    await bot.delete_message(message.chat.id, message.id)

@bot.callback_query_handler(func=lambda call: True)
@logger.catch
async def inline_func(call):
    if 'page' in call.data:
        message = call.message
        logger.info(f'{message.chat.id} | press page button')
        page = int(call.data[5:])

        products = await gen_product_button(page)
        pages = await gen_page_button(page)
        back_button = types.InlineKeyboardButton(text='Back', callback_data='back')

        markup = types.InlineKeyboardMarkup([*products, pages, [back_button]])

        try: await bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text='Products:', reply_markup=markup)
        except: ...
    elif 'id' in call.data:
        message = call.message
        logger.info(f'{message.chat.id} | press product button')

        id = call.data.split()[1]
        page = call.data.split()[3]

        name = await get_product_name(id)
        description = await get_product_description(id)
        price = str(await get_product_price(id))
        image = str(await get_product_image(id))

        text = f'{name}\n{price}\n{description}'
        btn1 = types.InlineKeyboardButton(text='Back', callback_data=f'products_back {page}')
        markup = types.InlineKeyboardMarkup([[btn1]])

        if image == '':
            await bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=text, reply_markup=markup)
        else:
            try:
                image = django_path + '/' + str(image)
                with open(image, 'rb') as f:
                    await bot.delete_message(message.chat.id, message.id)
                    await bot.send_photo(message.chat.id, f, caption=text, reply_markup=markup)
            except: await bot.send_message(message.chat.id, 'Clear the chat and restart the bot.')
    elif 'products_back' in call.data:
        message = call.message
        logger.info(f'{message.chat.id} | press "Back" in product')
        page = int(call.data.split()[1])

        products = await gen_product_button(page)
        pages = await gen_page_button(page)
        back_button = types.InlineKeyboardButton(text='Back', callback_data='back')

        markup = types.InlineKeyboardMarkup([*products, pages, [back_button]])

        try: 
            await bot.delete_message(message.chat.id, message.id)
            await bot.send_message(chat_id=message.chat.id, text='Products:', reply_markup=markup)
        except: await bot.send_message(message.chat.id, 'Clear the chat and restart the bot.')

    elif call.data == 'products':
        message = call.message
        logger.info(f'{message.chat.id} | press "Products"')

        products = await gen_product_button(1)
        pages = await gen_page_button(1)
        back_button = types.InlineKeyboardButton(text='Back', callback_data='back')

        markup = types.InlineKeyboardMarkup([*products, pages, [back_button]])

        await bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text='Products:', reply_markup=markup)
    elif call.data == 'back':
        message = call.message
        logger.info(f'{message.chat.id} | press "Back"')

        btn1 = types.InlineKeyboardButton('Products', callback_data='products')
        markup = types.InlineKeyboardMarkup([[btn1]])

        await bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text='Menu:', reply_markup=markup)

while True:
    try:
        logger.info("Start bot")
        asyncio.run(bot.polling(non_stop=True, interval=1, timeout=0))
    except KeyboardInterrupt:
        logger.info("Stopping the application")
        time.sleep(5)
    except Exception:
        logger.info("Something went wrong...")
        time.sleep(5)
