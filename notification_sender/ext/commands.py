from .database import db
from ..models import Channel, Status


def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


def seed_status():
    status = [
        Status(name='CREATED'),
        Status(name='QUEUED'),
        Status(name='SENT'),
        Status(name='NOT SENT')
    ]

    db.session.bulk_save_objects(status)
    db.session.commit()


def seed_channels():
    channels = [
        Channel(name='E-mail'),
        Channel(name='Telegram'),
        Channel(name='WhatsApp')
    ]

    db.session.bulk_save_objects(channels)
    db.session.commit()


def seed():
    seed_channels()
    seed_status()


def init_app(app):
    for command in [create_db, seed_status, seed_channels, seed]:
        app.cli.add_command(app.cli.command()(command))
