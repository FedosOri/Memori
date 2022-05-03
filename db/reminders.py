import sqlalchemy
from .db_session import SqlAlchemyBase


class Reminder(SqlAlchemyBase):
    __tablename__ = 'reminders'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user = sqlalchemy.Column(sqlalchemy.String)
    text = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    datetime = sqlalchemy.Column(sqlalchemy.String)
    chat_id = sqlalchemy.Column(sqlalchemy.String)
