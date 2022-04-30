import telebot
from telebot import types
from settings import config

bot = telebot.TeleBot(config.token)

new_note_step_1 = False
new_reminder_step_1 = False
new_reminder_step_2 = False


@bot.message_handler(commands=["start", "menu"])
def start(message):
    mes = "привет"
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
    global new_note_step_1
    new_note_step_1 = True
    mes = "введите содержание заметки:"
    bot.send_message(message.chat.id, mes, reply_markup=create_special_keyboard(["отмена"]))


@bot.message_handler(func=lambda message: new_note_step_1, content_types=["text"])
def create_new_note(message):
    global new_note_step_1
    new_note_step_1 = False
    if message.text == "отмена":
        mes = "отмена создания"
    else:
        # создать новую заметку
        mes = "заметка создана"
    bot.send_message(message.chat.id, mes, reply_markup=create_default_keyboard())


@bot.message_handler(commands=["reminders"])
def reminders(message):
    mes = ""
    # список напоминаний
    bot.send_message(message.chat.id, mes)


@bot.message_handler(commands=["new_reminder"])
def new_reminder(message):
    global new_reminder_step_1
    new_reminder_step_1 = True
    mes = "введите, что вам напомнить:"
    bot.send_message(message.chat.id, mes, reply_markup=create_special_keyboard(["отмена"]))


@bot.message_handler(func=lambda message: new_reminder_step_1, content_types=["text"])
def create_new_reminder_step_1(message):
    global new_reminder_step_1, new_reminder_step_2
    if message.text == "отмена":
        mes = "отмена создания"
    else:
        new_reminder_step_2 = True
        mes = "введите, когда вам напомнить:"
    new_reminder_step_1 = False
    bot.send_message(message.chat.id, mes, reply_markup=create_special_keyboard(["назад", "отмена"]))


@bot.message_handler(func=lambda message: new_reminder_step_2, content_types=["text"])
def create_new_reminder_step_1(message):
    global new_reminder_step_1, new_reminder_step_2
    if message.text == "отмена":
        mes = "отмена создания"
    elif message.text == "назад":
        new_reminder_step_1 = True
        mes = "введите, что вам напомнить:"
    else:
        # создать напоминание
        mes = "напоминание создано"
    new_reminder_step_2 = False
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
    item4 = types.KeyboardButton("/new_reminder")
    item5 = types.KeyboardButton("/menu")
    item6 = types.KeyboardButton("/help")
    keyboard.add(item1, item2, item3, item4, item5, item6)
    return keyboard


def create_special_keyboard(items):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in items:
        keyboard.add(types.KeyboardButton(item))
    return keyboard


bot.polling(none_stop=True)
