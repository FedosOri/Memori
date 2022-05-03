from db.notes import Note
from db.reminders import Reminder
from db import db_session


def get_all_notes(name):
    db_sess = db_session.create_session()
    notes = db_sess.query(Note).filter(Note.user == name).all()
    return notes


def new_note(user, text):
    db_sess = db_session.create_session()
    notes = Note()
    notes.user = user
    notes.text = text
    db_sess.add(notes)
    db_sess.commit()


def get_all_reminders(name):
    db_sess = db_session.create_session()
    reminders = db_sess.query(Reminder).filter(Reminder.user == name).all()
    return reminders


def new_reminder(user, text, datetime, chat_id):
    db_sess = db_session.create_session()
    reminder = Reminder()
    reminder.user = user
    reminder.text = text
    reminder.datetime = datetime
    reminder.chat_id = chat_id
    db_sess.add(reminder)
    db_sess.commit()


def delete(where, i):
    db_sess = db_session.create_session()
    if where == "note":
        db_sess.query(Note).filter(Note.id == int(i)).delete()
        db_sess.commit()
    else:
        db_sess.query(Reminder).filter(Reminder.id == int(i)).delete()
        db_sess.commit()
