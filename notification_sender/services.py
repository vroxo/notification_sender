import pika
import sys
import random
from pika import exceptions
from notification_sender import LOGGER
from .vo import PublishableMessageVo, ChannelVo


class MessageQueueProducerService:
    def __init__(self, credentials, exchange):
        self.credentials = pika.PlainCredentials(credentials.get('user'), credentials.get('password'))
        self.parameters = pika.ConnectionParameters(host=credentials.get('host'), credentials=self.credentials)
        self.exchange_name = exchange.get('name')
        self.exchange_type = exchange.get('type')

    def _connect(self) -> pika.BlockingConnection:
        return pika.BlockingConnection(self.parameters)

    def _create_channel(self, connection: pika.BlockingConnection) -> pika.adapters.blocking_connection.BlockingChannel:
        return connection.channel()

    def _declare_exchange(self, channel: pika.adapters.blocking_connection.BlockingChannel):
        channel.exchange_declare(exchange=self.exchange_name, exchange_type=self.exchange_type)

    def _close_connection(self, connection: pika.BlockingConnection):
        connection.close()

    def _publish_message(self, channel: pika.adapters.blocking_connection.BlockingChannel,
                         message: PublishableMessageVo):
        channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self._get_routing_key(message.channel),
            body=message.get_json()
        )
        LOGGER.info(f'Message Queued: {message.get_json()}')

    def send_message(self, message: PublishableMessageVo):
        try:
            conn = self._connect()
            channel = self._create_channel(conn)
            self._declare_exchange(channel)
            self._publish_message(channel, message)
            self._close_connection(conn)
        except exceptions.AMQPError as err:
            raise Exception(f'{__name__} Error! - {err.__repr__()}')

    @staticmethod
    def _get_routing_key(channel: ChannelVo) -> str:
        return f"{channel.name.lower()}.{random.randint(0, sys.maxsize)}"
