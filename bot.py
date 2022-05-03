import telebot
import datetime

from db import db_session
from telebot import types
from settings import config
from db import db_help

bot = telebot.TeleBot(config.token)
db_session.global_init("db/database.db")

notes_list_active = False
notes_delete = False
new_note_step_1 = False

reminders_list_active = False
reminders_delete = False
new_reminder_step_1 = False
new_reminder_step_2 = False
new_reminder_text = ""


@bot.message_handler(commands=["start", "menu"])
def start(message):
    global notes_list_active, notes_delete, new_note_step_1,\
        reminders_list_active, reminders_delete, new_reminder_step_1, new_reminder_step_2, new_reminder_text
    notes_list_active = False
    notes_delete = False
    new_note_step_1 = False

    reminders_list_active = False
    reminders_delete = False
    new_reminder_step_1 = False
    new_reminder_step_2 = False
    new_reminder_text = ""

    mes = "привет, я бот который поможет ничего не забыть и сделать важные заметки!"
    bot.send_message(message.chat.id, mes, reply_markup=create_default_keyboard())


@bot.message_handler(commands=["notes"])
def notes_list(message):
    global notes_list_active
    notes = db_help.get_all_notes(message.from_user.username)
    if len(notes):
        notes_list_active = True
        mes = "список ваших заметок "
        mes += "(" + str(len(notes)) + "/6):"
        bot.send_message(message.chat.id, mes, reply_markup=create_special_keyboard(["/delete", "/menu"]))
        for n in notes:
            note = f"\nid: {n.id}\ntext: {n.text}"
            bot.send_message(message.chat.id, note)
    else:
        mes = "вы еще не создали ни одной заметки"
        bot.send_message(message.chat.id, mes)


@bot.message_handler(commands=["new_note"])
def new_note(message):
    global new_note_step_1
    if len(db_help.get_all_notes(message.from_user.username)) <= 5:
        new_note_step_1 = True
        mes = "введите содержание заметки:"
        bot.send_message(message.chat.id, mes, reply_markup=create_special_keyboard(["отмена"]))
    else:
        mes = "вы уже создали 6 заметок"
        bot.send_message(message.chat.id, mes, reply_markup=create_default_keyboard())


@bot.message_handler(func=lambda message: new_note_step_1, content_types=["text"])
def create_new_note(message):
    global new_note_step_1
    new_note_step_1 = False
    if message.text == "отмена":
        mes = "отмена создания"
    else:
        db_help.new_note(message.from_user.username, message.text)
        mes = "заметка создана"
    bot.send_message(message.chat.id, mes, reply_markup=create_default_keyboard())


@bot.message_handler(commands=["reminders"])
def reminders_list(message):
    global reminders_list_active
    reminders = db_help.get_all_reminders(message.from_user.username)
    if len(reminders):
        reminders_list_active = True
        mes = "список ваших напоминаний "
        mes += "(" + str(len(reminders)) + "/6):"
        bot.send_message(message.chat.id, mes, reply_markup=create_special_keyboard(["/delete", "/menu"]))
        for n in reminders:
            dt = n.datetime.split()
            str_dt = dt[0] + "." + dt[1] + "." + dt[2] + " " + dt[3] + ":" + dt[4]
            note = f"\nid: {n.id}\ndate_and_time: {str_dt}\ntext: {n.text}"
            bot.send_message(message.chat.id, note)
    else:
        mes = "вы еще не создали ни одного напоминания"
        bot.send_message(message.chat.id, mes)


@bot.message_handler(commands=["new_reminder"])
def new_reminder(message):
    global new_reminder_step_1
    if len(db_help.get_all_reminders(message.from_user.username)) <= 5:
        new_reminder_step_1 = True
        mes = "введите, что вам напомнить:"
        bot.send_message(message.chat.id, mes, reply_markup=create_special_keyboard(["мне нужно кое-что сделать",
                                                                                     "отмена"]))
    else:
        mes = "вы уже создали 6 напоминаний"
        bot.send_message(message.chat.id, mes, reply_markup=create_default_keyboard())


@bot.message_handler(func=lambda message: new_reminder_step_1, content_types=["text"])
def create_new_reminder_step_1(message):
    global new_reminder_step_1, new_reminder_step_2, new_reminder_text
    if message.text == "отмена":
        mes = "отмена создания"
        bot.send_message(message.chat.id, mes, reply_markup=create_default_keyboard())
    else:
        new_reminder_step_2 = True
        new_reminder_text = message.text
        mes = "введите, когда вам напомнить\n" \
              "(выберете из предложенного или введите в формате:\n" \
              "день месяц год и точное время через пробел,\n" \
              "например, 1 1 2111 11 11)"
        bot.send_message(message.chat.id, mes,
                         reply_markup=create_special_keyboard(
                             ["через 15 минут", "через 1 час", "через 4 часа", "назад", "отмена"]
                         ))
    new_reminder_step_1 = False


@bot.message_handler(func=lambda message: new_reminder_step_2, content_types=["text"])
def create_new_reminder_step_2(message):
    global new_reminder_step_1, new_reminder_step_2, new_reminder_text
    if message.text == "отмена":
        mes = "отмена создания"
        bot.send_message(message.chat.id, mes, reply_markup=create_default_keyboard())
        new_reminder_step_2 = False
    elif message.text == "назад":
        new_reminder_step_1 = True
        mes = "введите, что вам напомнить:"
        bot.send_message(message.chat.id, mes, reply_markup=create_special_keyboard(["отмена"]))
        new_reminder_step_2 = False
    else:
        if message.text == "через 15 минут":
            shift = datetime.datetime.now() + datetime.timedelta(minutes=50)
            shift = shift.timetuple()
            dt = str(shift[2]) + " " + str(shift[1]) + " " + str(shift[0]) + " " + str(shift[3]) + " " + str(
                shift[4])
        elif message.text == "через 1 час":
            shift = datetime.datetime.now() + datetime.timedelta(hours=1)
            shift = shift.timetuple()
            dt = str(shift[2]) + " " + str(shift[1]) + " " + str(shift[0]) + " " + str(shift[3]) + " " + str(
                shift[4])
        elif message.text == "через 4 час":
            shift = datetime.datetime.now() + datetime.timedelta(hours=4)
            shift = shift.timetuple()
            dt = str(shift[2]) + " " + str(shift[1]) + " " + str(shift[0]) + " " + str(shift[3]) + " " + str(
                shift[4])
        else:
            dt = message.text
        check_format_datetime(dt, message)


@bot.message_handler(commands=["delete"])
def delete(message):
    global notes_list_active, notes_delete, reminders_list_active, reminders_delete
    if notes_list_active:
        notes_list_active = False
        notes_delete = True
        notes = [str(n.id) for n in db_help.get_all_notes(message.from_user.username)] + ["отмена"]
        mes = "введите id заметки, которую хотите удалить:"
        bot.send_message(message.chat.id, mes, reply_markup=create_special_keyboard(notes))
    elif reminders_list_active:
        reminders_list_active = False
        reminders_delete = True
        reminders = [str(r.id) for r in db_help.get_all_reminders(message.from_user.username)] + ["отмена"]
        mes = "введите id напоминания, которое хотите удалить:"
        bot.send_message(message.chat.id, mes, reply_markup=create_special_keyboard(reminders))


@bot.message_handler(func=lambda message: notes_delete, content_types=["text"])
def delete_note(message):
    global notes_delete
    if message.text == "отмена":
        mes = "отмена удаления"
        bot.send_message(message.chat.id, mes, reply_markup=create_default_keyboard())
        notes_delete = False
    else:
        notes = [str(n.id) for n in db_help.get_all_notes(message.from_user.username)]
        if message.text in notes:
            db_help.delete("note", message.text)
            notes_delete = False
            mes = "заметка удалена"
            bot.send_message(message.chat.id, mes, reply_markup=create_default_keyboard())
        else:
            mes = "такой заметки не существует"
            bot.send_message(message.chat.id, mes)


@bot.message_handler(func=lambda message: reminders_delete, content_types=["text"])
def delete_reminder(message):
    global reminders_delete
    if message.text == "отмена":
        mes = "отмена удаления"
        bot.send_message(message.chat.id, mes, reply_markup=create_default_keyboard())
        reminders_delete = False
    else:
        reminders = [str(r.id) for r in db_help.get_all_reminders(message.from_user.username)]
        if message.text in reminders:
            db_help.delete("reminder", message.text)
            reminders_delete = False
            mes = "напоминание удалено"
            bot.send_message(message.chat.id, mes, reply_markup=create_default_keyboard())
        else:
            mes = "такого напоминания не существует"
            bot.send_message(message.chat.id, mes)


def create_default_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/notes")
    item2 = types.KeyboardButton("/new_note")
    item3 = types.KeyboardButton("/reminders")
    item4 = types.KeyboardButton("/new_reminder")
    item5 = types.KeyboardButton("/menu")
    keyboard.add(item1, item2, item3, item4, item5)
    return keyboard


def create_special_keyboard(items):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for item in items:
        keyboard.add(types.KeyboardButton(item))
    return keyboard


def check_format_datetime(dt, message):
    global new_reminder_step_1, new_reminder_step_2, new_reminder_text
    true_format = dt.split()
    if len(true_format) == 5:
        if 1 <= int(true_format[3]) <= 23 and 1 <= int(true_format[4]) <= 59:
            if true_format[1] == "2":
                if 1 <= int(true_format[0]) <= 28:
                    db_help.new_reminder(message.from_user.username, new_reminder_text, dt, message.chat.id)
                    mes = "напоминание создано"
                    bot.send_message(message.chat.id, mes, reply_markup=create_default_keyboard())
                    new_reminder_step_2 = False
                else:
                    mes = "неправильный формат даты"
                    bot.send_message(message.chat.id, mes)
            elif true_format[1] in ["1", "3", "5", "7", "8", "10", "12"]:
                if 1 <= int(true_format[0]) <= 31:
                    db_help.new_reminder(message.from_user.username, new_reminder_text, dt, message.chat.id)
                    mes = "напоминание создано"
                    bot.send_message(message.chat.id, mes, reply_markup=create_default_keyboard())
                    new_reminder_step_2 = False
                else:
                    mes = "неправильный формат даты"
                    bot.send_message(message.chat.id, mes)
            elif true_format[1] in ["4", "6", "9", "11"]:
                if 1 <= int(true_format[0]) <= 30:
                    db_help.new_reminder(message.from_user.username, new_reminder_text, dt, message.chat.id)
                    mes = "напоминание создано"
                    bot.send_message(message.chat.id, mes, reply_markup=create_default_keyboard())
                    new_reminder_step_2 = False
                else:
                    mes = "неправильный формат даты"
                    bot.send_message(message.chat.id, mes)
            else:
                mes = "неправильный формат даты"
                bot.send_message(message.chat.id, mes)
        else:
            mes = "неправильный формат даты"
            bot.send_message(message.chat.id, mes)
    else:
        mes = "неправильный формат даты"
        bot.send_message(message.chat.id, mes)


bot.polling(none_stop=True)
