from .vo import *
from .models import *


class SendRepository:

    @staticmethod
    def create_send(request: RequestVo) -> PublishableMessageVo:
        channel = SendRepository.get_channel_by_id(request.channel)
        message = SendRepository.create_message(request.text)

        senders = list()
        for user in request.users:
            sender = SendRepository.create_sender(channel, message, user)
            senders.append(SenderVo(id=sender.id, address=sender.address).get_json())

        message_to_queue = PublishableMessageVo(ChannelVo(id=channel.id, name=channel.name),
                                                MessageVo(id=message.id, text=message.text),
                                                senders)

        return message_to_queue

    @staticmethod
    def create_sender(channel: Channel, message: Message, user: str) -> Sender:
        sender = Sender(status_id=1, address=user)
        sender.channel = channel
        sender.message = message

        db.session.add(sender)
        db.session.commit()

        return sender

    @staticmethod
    def get_channel_by_id(channel_id: int) -> Channel:
        channel = Channel.query.filter_by(id=channel_id).one()
        return channel

    @staticmethod
    def create_message(text: str) -> Message:
        message = Message(text=text)

        db.session.add(message)
        db.session.commit()

        return message

    @staticmethod
    def mark_message_queued(publishable_message: PublishableMessageVo):
        db.session.query(Sender).filter(Sender.message_id == publishable_message.message.id).update(
            {Sender.status_id: 2})
        db.session.commit()
