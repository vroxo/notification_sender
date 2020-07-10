import pytest
from unittest.mock import Mock
from pika.exceptions import AMQPError

from notification_sender.services import MessageQueueProducerService
from notification_sender.vo import MessageVo, ChannelVo, PublishableMessageVo, SenderVo


class TestMessageQueueProducer:
    @pytest.fixture
    def credentials(self):
        return Mock(username='username', password='password')

    @pytest.fixture
    def parameters(self, credentials):
        return Mock(host='host', credentials=credentials)

    @pytest.fixture
    def producer_object(self, mocker, credentials, parameters):
        mocker.patch('notification_sender.services.pika.PlainCredentials', return_value=credentials)
        mocker.patch('notification_sender.services.pika.ConnectionParameters', return_value=parameters)
        return MessageQueueProducerService(credentials, dict(name='exanche_name', type='exanche_type'))

    @pytest.fixture
    def message(self):
        return PublishableMessageVo(
            channel=ChannelVo(id=1, name='E-mail'),
            message=MessageVo(id=1, text='This is a notification message for one or more users'),
            senders=[SenderVo(id=1, address='usar@gmail.com').get_json()]
        )

    def test_get_routing_queue(self, message):
        routing_key = MessageQueueProducerService._get_routing_key(message.channel)

        assert 'e-mail.' in routing_key[:7]

    def test_connect(self, mocker, producer_object):
        pika_mock = mocker.patch('notification_sender.services.pika')
        producer_object._connect()
        pika_mock.BlockingConnection.assert_called_once_with(producer_object.parameters)

    def test_close_connection(self, mocker, producer_object):
        conn = mocker.patch('notification_sender.services.pika.BlockingConnection')
        producer_object._close_connection(conn)
        conn.close.assert_called()

    def test_create_channel(self, mocker, producer_object):
        conn = mocker.patch('notification_sender.services.pika.BlockingConnection')
        producer_object._create_channel(conn)
        conn.channel.assert_called()

    def test_declare_exchange(self, mocker, producer_object):
        channel = mocker.patch('notification_sender.services.pika.BlockingConnection.channel')
        producer_object._declare_exchange(channel)
        channel.exchange_declare.assert_called_once_with(exchange=producer_object.exchange_name,
                                                         exchange_type=producer_object.exchange_type)

    def test_publish_message_queue(self, mocker, producer_object, message):
        channel = mocker.patch('notification_sender.services.pika.BlockingConnection.channel')
        producer_object._publish_message(channel, message)
        channel.basic_publish.assert_called()

    def test_send_message_to_queue(self, mocker, producer_object, message):
        _connect = mocker.patch('notification_sender.services.MessageQueueProducerService._connect')
        _create_channel = mocker.patch('notification_sender.services.MessageQueueProducerService._create_channel')
        _declare_exchange = mocker.patch('notification_sender.services.MessageQueueProducerService._declare_exchange')
        _publish_message = mocker.patch('notification_sender.services.MessageQueueProducerService._publish_message')
        _close_connection = mocker.patch('notification_sender.services.MessageQueueProducerService._close_connection')

        producer_object.send_message(message)

        _connect.assert_called()
        _create_channel.assert_called()
        _declare_exchange.assert_called()
        _publish_message.assert_called()
        _close_connection.assert_called()

    def test_send_message_except_amqp_error_raise_exception(self, mocker, producer_object, message):
        mocker.patch('notification_sender.services.MessageQueueProducerService._connect', side_effect=AMQPError)
        with pytest.raises(Exception):
            producer_object.send_message(message)
