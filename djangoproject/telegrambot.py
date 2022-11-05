import telebot
from telebot import types
import asyncio
from asgiref.sync import sync_to_async
from telebot.async_telebot import AsyncTeleBot
from loguru import logger
import time, math

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

import django
django.setup()
from django.core.management.base import BaseCommand
from products.models import ProductsList


logger.add('logs/bot.log', format='{time} {level} {message}')

token = '5669662526:AAF5IKDO18_A293S-hEgqPsSdv86HjC5JGM'
bot = AsyncTeleBot(token)

@bot.message_handler(commands=['start', 'help'])
@logger.catch
async def send_welcome(message):
    logger.info(f'{str(message.chat.id)} | start bot')
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Products')

    markup.add(btn1)
    await bot.send_message(message.chat.id, f'Hello {message.from_user.first_name}', reply_markup = markup)
    await bot.delete_message(message.chat.id, message.id)

@logger.catch
async def gen_product_button(page=int):
    page -= 1
    if page > 0: page = int(str(page) + '0')

    products = []
    for i in range(await sync_to_async(ProductsList.objects.count)()):
        if len(products) == 10 or page + (i + 1) > await sync_to_async(ProductsList.objects.count)():
            break
        product = await sync_to_async(ProductsList.objects.get)(id=(page + (i + 1)))
        products.append([types.InlineKeyboardButton(text=product.product_name, callback_data=str(i + 1))])

    return products

@logger.catch
async def gen_page_button(page=int):
    page_index = page - 2
    if page_index < 1: page_index = 1
    pages = []
    page_count = math.ceil(await sync_to_async(ProductsList.objects.count)() / 10)

    btn1 = types.InlineKeyboardButton(text='<<', callback_data='<<')
    btn2 = types.InlineKeyboardButton(text=f'>>', callback_data='>>')
    
    pages.append(btn1)
    for i in range(page_count):
        if i == 5:
            break
        pages.append(types.InlineKeyboardButton(text=str(page_index + i), callback_data=str(page_index + i)))
    pages.append(btn2)

    return pages

@bot.message_handler(content_types=['text'])
@logger.catch
async def bot_func(message):
    if message.text == 'Products':
        logger.info(f'{message.chat.id} | press "Products"')
        
        
        products = await gen_product_button(1)
        pages = await gen_page_button(1)
        
        markup = types.InlineKeyboardMarkup([*products, pages])

        await bot.send_message(message.chat.id, 'Products:', reply_markup=markup)
        await bot.delete_message(message.chat.id, message.id)

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