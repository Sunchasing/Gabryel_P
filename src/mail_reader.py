import base64
from lib.logging.gabryel_logger import get_logger
from src.service_manager import ServiceManager


class GMailReader:
    logger = get_logger()
    _SVC = ServiceManager.get_service('gmail').users().messages()
    _UID = 'me'

    def __init__(self, user_id):
        self._UID = user_id

    @classmethod
    def get_unread_mail_ids(cls):
        cls.logger.info('Getting message IDs...')
        try:
            response = cls._SVC.list(userId=cls._UID, labelIds=['UNREAD']).execute()
            cls.logger.debug('Successful response')
            message_ids = []

            if 'messages' in response:
                message_ids.extend(response['messages'])

            for i, header in enumerate(message_ids):
                message_ids[i] = header.get('id')

            cls.logger.debug(f'Got message IDs: {", ".join(message_ids)}')
            return message_ids

        except Exception as e:
            try:
                ServiceManager.refresh_service()
            except: ...
            cls.logger.exception(f'Exception caught in get_unread_mail_ids: {e}')
            return []

    @classmethod
    def get_message_by_id_if_squarespace(cls, find_str_in_message, find_second_str_in_message, message_id):
        cls.logger.info(f'Checking message with ID {message_id}')
        try:
            message = cls._SVC.get(userId=cls._UID, id=message_id, format='raw').execute()
            msg = str(base64.urlsafe_b64decode(message['raw'].encode('ASCII')))
            if find_str_in_message in msg and find_second_str_in_message in msg:
                cls.logger.info('Found an order message! Passing on...')
                cls.logger.debug(f'Message: {msg}')
                return msg
            else:
                cls.logger.debug('Not an order, ignoring..')
                return None

        except Exception as e:
            cls.logger.exception(f'Exception caught in get_message_by_id_if_squarespace: {e}',
                                 find_str_in_message, find_second_str_in_message, message_id)
            return None

    @classmethod
    def get_messages_from_squarespace(cls, message_ids: list, find_str_in_message='', find_second_str_in_message=''):
        list_of_messages = []
        sqsp_message_ids = []
        for message_id in message_ids:
            message = cls.get_message_by_id_if_squarespace(find_str_in_message, find_second_str_in_message, message_id)
            if message:
                list_of_messages.append(message)
                sqsp_message_ids.append(message_id)
        return list_of_messages, sqsp_message_ids

    @classmethod
    def mark_as_read(cls, message_id):
        try:
            cls.logger.debug(f'Setting message {message_id} to read..')
            cls._SVC.modify(userId=cls._UID, id=message_id, body={'removeLabelIds': ['UNREAD']}).execute()
        except Exception as e:
            cls.logger.exception(f'Exception caught in mark_as_read: {e}', message_id)
