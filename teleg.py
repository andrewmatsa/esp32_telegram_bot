#esptool --chip esp32 --port COM4 --baud 460800 write_flash -z 0x1000 esp32-20220618-v1.19.1.bin
# https://api.telegram.org/bot5961538933:AAF9EtEI30gZmpGsD9yqHX5i2UANJg_kRHs/getUpdates
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Unrestricted -Force
# Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass -Force
import telegram
from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, bot
from telegram.ext import *
import keys
import time
import random

from main import measure_temp_and_hum

print(f'Starting bot rend numb is {random.randint(0,10)}...')


check_voltage = "Check voltage"
start_debug_mode = "Select debug mode"
view_devices = "View devices"


def start(update, context):
    buttons = [[KeyboardButton(check_voltage)],
               [KeyboardButton(start_debug_mode)],
               [KeyboardButton(view_devices)]
               ]
    context.bot.send_message(chat_id=update.effective_chat.id, text="hello, welcome to matsa esp tool for monitoring your esp devices",
                             reply_markup=ReplyKeyboardMarkup(keyboard=buttons,
                                                              resize_keyboard=True))


def time_to_execute(timer=10):
    i = int(time.time())+timer
    while int(time.time()) <= i:
        print(f'Exit on "{timer}" seconds')

def list(update, context):
    update.message.reply_text('some list of devices what you added')

def handle_message(update, context):
    if check_voltage in update.message.text:
        response = 'Checking voltage function'
        mth = measure_temp_and_hum()
        print(mth)
        # send_message(f"Temperature: {mth.get('temp')}", CHAT_ID)
    if start_debug_mode in update.message.text:
        timer = 10
        i = int(time.time()) + timer
        while int(time.time()) <= i:

            print(f'Exit on "{timer}" seconds')
        response = 'Starting debug mode'
    if view_devices in update.message.text:
        response = 'Device view'
    if 'hello' in update.message.text:
        response = "Hey there, choose what you would like to do!"

    update.message.reply_text(response)

def error(update, context):
    print(f"Update {update} caused error {context.error}")



if __name__ == '__main__':
    updater = Updater(keys.token, use_context=True)
    dp = updater.dispatcher

    # commands
    dp.add_handler(CommandHandler('start', start))

    # messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # error handler
    dp.add_error_handler(error)

    # Run bot
    updater.start_polling(1.0)
    updater.idle()
