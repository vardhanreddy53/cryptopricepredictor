from . import db_2
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db_2.Model):
    id = db_2.Column(db_2.Integer, primary_key=True)
    data = db_2.Column(db_2.String(10000))
    date = db_2.Column(db_2.DateTime(timezone=True), default=func.now())
    user_id = db_2.Column(db_2.Integer, db_2.ForeignKey('user.id'))


class User(db_2.Model, UserMixin):
    id = db_2.Column(db_2.Integer, primary_key=True)
    email = db_2.Column(db_2.String(150), unique=True)
    password = db_2.Column(db_2.String(150))
    first_name = db_2.Column(db_2.String(150))
    notes = db_2.relationship('Note')
