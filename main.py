from time import sleep
from config.configuration import Configuration
from lib.logging import gabryel_logger
from src.google_calendar_event_creator import GoogleCalendarHandler
from src.mail_parser import MailParser as mparser
from src.mail_reader import GMailReader as mreader

logger = gabryel_logger.get_logger()

checked_message_id_cache = set()


def main():
    list_of_ids = mreader.get_unread_mail_ids()
    new_ids = [x for x in list_of_ids if x not in checked_message_id_cache]
    list_of_messages, sqsp_msg_ids = mreader.get_messages_from_squarespace(new_ids,
                                                                           Configuration.SENDER_EMAIL,
                                                                           Configuration.DEFAULT_MESSAGE_BEGINNING)
    for x in sqsp_msg_ids:
        logger.debug(x)
        new_ids.remove(x)
    checked_message_id_cache.update(new_ids)
    if sqsp_msg_ids:
        parsed_messages = [mparser.strip_message(message) for message in list_of_messages]
        list_of_orders = [mparser.create_client_dictionary(message) for message in parsed_messages]
        estimated = []
        event_dict = []
        for field in list_of_orders:
            event_dict.append(field[0])
            estimated.append(field[1])
        return event_dict, estimated, parsed_messages, sqsp_msg_ids
    else:
        logger.info('No new messages found...')
        return [], [], [], []


if __name__ == '__main__':
    while True:
        try:
            event_dict, estimated, original_message, sqsp_msg_ids = main()

            for est, dic, msg, id in zip(estimated, event_dict, original_message, sqsp_msg_ids):
                GoogleCalendarHandler.create_event(est, dic, msg)
                mreader.mark_as_read(id)
        except Exception as e:
            logger.exception(f'Caught general exception in main loop: {e}')
        finally:
            sleep(60)
