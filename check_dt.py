import datetime
import telebot
import time

from db.reminders import Reminder
from db import db_session
from db import db_help
from settings import config


# def check(dt):
#     print(dt)
#     dt = dt.split()
#     hour = int(dt[3])
#     minute = int(dt[4])
#     d = int(dt[0])
#     m = int(dt[1])
#     y = int(dt[2])
#
#     dt_now = datetime.datetime.now()
#     hour_now = dt_now.hour
#     minute_now = dt_now.minute
#     d_now = dt_now.day
#     m_now = dt_now.month
#     y_now = dt_now.year
#
#     if y == y_now:
#         if m == m_now:
#             if d == d_now:
#                 if hour == hour_now:
#                     if minute <= minute_now:
#                         return True
#                 elif hour < hour_now:
#                     return True
#             elif d < d_now:
#                 return True
#         elif m < m_now:
#             return True
#     elif y < y_now:
#         return True
#     return False


def check(dt):
    dt = dt.split()
    year = str(dt[0])  # [2]
    month = str(dt[1])  # [1]
    day = str(dt[2])  # [0]
    hour = str(dt[3])  # [3]
    minute = str(dt[4])  # [4]
    time_now = datetime.datetime.now()
    if str(time_now.year) >= year:
        if str(time_now.month) >= month or (str(time_now.month) < month and str(time_now.year) > year):
            if str(time_now.day) >= day or (str(time_now.day) < day and str(time_now.month) > month or (str(time_now.day) < day and str(time_now.year) > year or ())):
                if str(time_now.hour) >= hour or (str(time_now.hour) < hour and str(time_now.day) > day or (str(time_now.hour) < hour and str(time_now.month) > month or (str(time_now.hour) < hour and str(time_now.year) > year))):
                    if str(time_now.minute) >= minute or (str(time_now.minute) < minute and str(time_now.hour) > hour or (str(time_now.minute) < minute and str(time_now.day) > day or (str(time_now.minute) < minute and str(time_now.month) > month or (str(time_now.minute) < minute and str(time_now.year) > year)))):
                        return True
    return False


db_session.global_init("db/database.db")
bot = telebot.TeleBot(config.token)
while True:
    db_sess = db_session.create_session()
    reminders = db_sess.query(Reminder).all()
    for r in reminders:
        if check(r.datetime):
            bot.send_message(r.chat_id, r.text)
            db_help.delete("reminder", r.id)
    time.sleep(60)
