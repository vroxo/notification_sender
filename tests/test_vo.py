import pytest
import json
from notification_sender.vo import *


@pytest.fixture(scope="module")
def request_dict():
    return {'channel': 1, 'text': 'Teste!', 'users': ['user1', 'user2']}


@pytest.fixture(scope="module")
def message_dict():
    return {'id': 1, 'text': 'Teste!'}


@pytest.fixture(scope="module")
def channel_dict():
    return {'id': 1, 'name': 'Teste!'}


@pytest.fixture(scope="module")
def sender_dict():
    return {'id': 1, 'address': 'User1'}


class TestRequestVo:
    def test_construct(self, request_dict):
        request = RequestVo(**request_dict)
        assert isinstance(request, RequestVo)
        assert request.text == 'Teste!'
        assert request.channel == 1
        assert request.users == ['user1', 'user2']

    def test_get_json(self, request_dict):
        request = RequestVo(**request_dict)
        assert json.dumps(request_dict) == request.get_json()


class TestMessageVo:
    def test_construct(self, message_dict):
        message = MessageVo(**message_dict)
        assert isinstance(message, MessageVo)
        assert message.text == 'Teste!'
        assert message.id == 1

    def test_get_json(self, message_dict):
        message = MessageVo(**message_dict)
        assert json.dumps(message_dict) == message.get_json()


class TestChannelVo:
    def test_construct(self, channel_dict):
        channel = ChannelVo(**channel_dict)
        assert isinstance(channel, ChannelVo)
        assert channel.name == 'Teste!'
        assert channel.id == 1

    def test_get_json(self, channel_dict):
        channel = ChannelVo(**channel_dict)
        assert json.dumps(channel_dict) == channel.get_json()


class TestSenderVo:
    def test_construct(self, sender_dict):
        sender = SenderVo(**sender_dict)
        assert isinstance(sender, SenderVo)
        assert sender.address == 'User1'
        assert sender.id == 1

    def test_get_json(self, sender_dict):
        sender = SenderVo(**sender_dict)
        assert json.dumps({'id': 1, 'address': 'User1',
                           'url_update_sender': f'http://localhost:5000/api/v1/sent/{sender.id}'}) == sender.get_json()


class TestPublishableMessageVo:
    @pytest.fixture()
    def publishable_message(self, channel_dict, message_dict, sender_dict):
        return PublishableMessageVo(channel=ChannelVo(**channel_dict), message=MessageVo(**message_dict),
                                    senders=[SenderVo(**sender_dict).get_json()])

    def test_construct(self, publishable_message):
        assert isinstance(publishable_message, PublishableMessageVo)
        assert isinstance(publishable_message.message, MessageVo)
        assert isinstance(publishable_message.channel, ChannelVo)
        assert isinstance(publishable_message.senders, list)

    def test_get_json(self, publishable_message):
        json_message = publishable_message.get_json()

        assert publishable_message.message.text in json_message
        assert publishable_message.channel.name in json_message
        assert json.loads(publishable_message.senders[0])['address'] in json_message
