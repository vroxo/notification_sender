import datetime
from .ext.database import db


class Sender(db.Model):
    __tablename__ = "senders"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    message_id = db.Column(db.BigInteger, db.ForeignKey("messages.id"))
    channel_id = db.Column(db.BigInteger, db.ForeignKey("channels.id"))
    status_id = db.Column(db.Integer, db.ForeignKey("status.id"), default=1)
    address = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(),
                           onupdate=datetime.datetime.now())

    channel = db.relationship("Channel", back_populates="senders")
    message = db.relationship("Message", back_populates="senders")
    status = db.relationship("Status")


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    text = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    senders = db.relationship("Sender", back_populates='message')


class Channel(db.Model):
    __tablename__ = "channels"
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(35), nullable=False)

    senders = db.relationship("Sender", back_populates='channel')


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(35), nullable=False)
