import pytest

from notification_sender.vo import PublishableMessageVo, ChannelVo, MessageVo, SenderVo


class TestSender:
    @pytest.fixture
    def json_message(self):
        return dict(
            channel=1,
            text='This is a notification message for one or more users',
            users=['user1@gmail.com', 'user2@gmail.com']
        )

    @pytest.fixture
    def message(self):
        return PublishableMessageVo(ChannelVo(id=1, name='e-mail'),
                                    MessageVo(id=1, text='This is a notification message for one or more users'),
                                    [SenderVo(id=1, address='user1@gmail.com').get_json(),
                                     SenderVo(id=1, address='user2@gmail.com').get_json()])

    def test_send_post_valid_json_message(self, client, json_message, message, mocker):
        mocker.patch('notification_sender.repository.SendRepository.create_send', return_value=message)
        mocker.patch('notification_sender.services.MessageQueueProducerService.send_message')
        mocker.patch('notification_sender.repository.SendRepository.mark_message_queued')

        response = client.post('/api/v1/sender', json=json_message)

        assert response.status_code == 200
        assert response.json['error'] == False

    def test_send_post_invalid_json_message(self, client, json_message):
        json_message.pop('channel')
        response = client.post('/api/v1/sender', json=json_message)
        assert response.status_code == 400

    def test_send_blank_text(self, client, json_message):
        json_message['text'] = ''
        response = client.post('/api/v1/sender', json=json_message)
        assert response.status_code == 400

    def test_send_blank_channel(self, client, json_message):
        json_message['channel'] = ''
        response = client.post('/api/v1/sender', json=json_message)
        assert response.status_code == 400

    def test_send_empty_list_users(self, client, json_message):
        json_message['users'] = list()
        response = client.post('/api/v1/sender', json=json_message)
        assert response.status_code == 400

    def test_send_blank_list_users(self, client, json_message):
        json_message['users'] = ['', '']
        response = client.post('/api/v1/sender', json=json_message)
        assert response.status_code == 400

    def test_except_in_message_queue_producer_service_response_status_code_internal_error(self, mocker, json_message,
                                                                                          message, client):
        mocker.patch('notification_sender.repository.SendRepository.create_send', return_value=message)
        mocker.patch('notification_sender.repository.SendRepository.mark_message_queued')
        mocker.patch('notification_sender.services.MessageQueueProducerService.send_message', side_effect=Exception)
        response = client.post('/api/v1/sender', json=json_message)
        assert response.status_code == 500
        assert response.json['error']

    def test_except_in_create_send_response_status_code_internal_error(self, mocker, json_message, message, client):
        mocker.patch('notification_sender.repository.SendRepository.create_send', side_effect=Exception)
        mocker.patch('notification_sender.repository.SendRepository.mark_message_queued')
        mocker.patch('notification_sender.services.MessageQueueProducerService.send_message')

        response = client.post('/api/v1/sender', json=json_message)
        assert response.status_code == 500
        assert response.json['error']

    def test_except_in_mark_message_queued_response_status_code_internal_error(self, mocker, json_message, message,
                                                                               client):
        mocker.patch('notification_sender.repository.SendRepository.create_send', return_value=message)
        mocker.patch('notification_sender.repository.SendRepository.mark_message_queued', side_effect=Exception)
        mocker.patch('notification_sender.services.MessageQueueProducerService.send_message')

        response = client.post('/api/v1/sender', json=json_message)
        assert response.status_code == 500
        assert response.json['error']
