from notification_sender import LOGGER
from flask import make_response

from notification_sender.repository import SendRepository
from notification_sender.vo import *
from notification_sender.services import MessageQueueProducerService


def send(body):
    response_json = {"message": "Send message ok!", "error": False}
    try:
        request = RequestVo(**body)
        message = SendRepository.create_send(request)

        queue = MessageQueueProducerService({'user': 'admin', 'password': 'Admin123_', 'host': 'rabbitmq'},
                                            {'name': 'message_topic', 'type': 'topic'})

        queue.send_message(message)
        SendRepository.mark_message_queued(message)

        response = make_response(response_json, 200)

    except Exception as e:
        response_json['message'] = "Message not queued!"
        response_json['error'] = True
        response = make_response(response_json, 500)
        LOGGER.error(f"{__name__} - {e.__repr__()}")

    return response
