import json


class Vo:
    def get_json(self):
        return json.dumps(self.__dict__)


class RequestVo(Vo):
    def __init__(self, channel: int, text: str, users: list, *args, **kwargs):
        self.channel = channel
        self.text = text
        self.users = users


class ChannelVo(Vo):
    def __init__(self, id: int, name: str, *args, **kwargs):
        self.id = id
        self.name = name


class MessageVo(Vo):
    def __init__(self, id: int, text: str, *args, **kwargs):
        self.id = id
        self.text = text


class SenderVo(Vo):
    def __init__(self, id: int, address: str):
        self.id = id
        self.address = address
        self.url_update_sender = f'http://localhost:5000/api/v1/sent/{self.id}'


class PublishableMessageVo(Vo):
    def __init__(self, channel: ChannelVo, message: MessageVo, senders: list):
        self.channel = channel
        self.message = message
        self.senders = senders

    def get_json(self):
        return json.dumps(
            {'channel': self.channel.get_json(), 'message': self.message.get_json(),
             'seders': self.senders})
