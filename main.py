import telebot
from telebot import types
from data import config


bot = telebot.TeleBot(config.token)


@bot.message_handler(commands=["start", "menu"])
def start(message):
    mes = "Привет"
    bot.send_message(message.chat.id, mes, reply_markup=create_default_keyboard())


@bot.message_handler(commands=["help"])
def com_help(message):
    mes = ""
    bot.send_message(message.chat.id, mes, reply_markup=create_default_keyboard())


@bot.message_handler(commands=["notes"])
def notes(message):
    mes = ""
    # список заметок
    bot.send_message(message.chat.id, mes)


@bot.message_handler(commands=["new_note"])
def new_note(message):
    # создать новую заметку
    mes = "новая заметка создана"
    bot.send_message(message.chat.id, mes)


@bot.message_handler(commands=["reminders"])
def reminders(message):
    mes = ""
    # список напоминаний
    bot.send_message(message.chat.id, mes)


@bot.message_handler(commands=["new_reminder"])
def new_reminder(message):
    # создать новое напоминание
    mes = "новое напоминание создано"
    bot.send_message(message.chat.id, mes)


@bot.message_handler(commands=["change"])
def change(message):
    mes = ""
    bot.send_message(message.chat.id, mes)


@bot.message_handler(commands=["delete"])
def delete(message):
    mes = ""
    bot.send_message(message.chat.id, mes)


def create_default_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/notes")
    item2 = types.KeyboardButton("/new_note")
    item3 = types.KeyboardButton("/reminders")
    item4 = types.KeyboardButton("/new_reminders")
    item5 = types.KeyboardButton("/menu")
    item6 = types.KeyboardButton("/help")
    keyboard.add(item1, item2, item3, item4, item5, item6)
    return keyboard


bot.polling(none_stop=True)
