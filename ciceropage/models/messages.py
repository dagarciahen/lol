from datetime import datetime

from db import db
from . import User


class Message(db.Model):
    __tablename__ = 'messages'

    message_id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    sender_id = db.Column(db.Integer, db.ForeignKey(User.user_id))
    recipient_id = db.Column(db.Integer, db.ForeignKey(User.user_id))

    sender = db.relationship(User, foreign_keys=sender_id)
    recipient = db.relationship(User, foreign_keys=recipient_id)
