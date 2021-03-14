from config.configuration import Configuration
from lib.logging.gabryel_logger import get_logger
from src.pickup_dropoff_time import EventTimeNormalizer as etn


class MailParser:
    logger = get_logger()

    @classmethod
    def strip_message(cls,
                      message,
                      string_to_filter_from=Configuration.DEFAULT_MESSAGE_BEGINNING,
                      string_to_filter_to=Configuration.DEFAULT_MESSAGE_ENDING):
        cls.logger.info(f'Stripping message from {Configuration.DEFAULT_MESSAGE_BEGINNING}'
                        f' to {Configuration.DEFAULT_MESSAGE_ENDING}...')
        cls.logger.debug(f'Message: {message}')

        try:
            message.split(r'\r\n')

            get_from_index = message.index(string_to_filter_from) if string_to_filter_from in message else 0
            get_to_index = message.index(string_to_filter_to) if string_to_filter_to in message else len(message)

            return message[get_from_index:get_to_index].replace('\\', '')\
                                                       .replace('\\', '')\
                                                       .replace('rnrn', ' ')\
                                                       .replace('*', '')\
                                                       .replace(r'<p>', '')\
                                                       .replace('        ', ' ')\
                                                       .replace('<span>', '')
        except Exception as e:
            cls.logger.exception(f'Caught exception when calling strip_message: {e}',
                                 message, string_to_filter_from, string_to_filter_to)

    @classmethod
    def create_client_dictionary(cls, message):
        cls.logger.info('Creating client dict...')
        client_job = dict()
        for i in range(len(Configuration.DEFAULT_MAIL_FIELDS)):
            find_from = message.index(Configuration.DEFAULT_MAIL_FIELDS[i]) + len(Configuration.DEFAULT_MAIL_FIELDS[i]) + 1
            try:
                find_to = message.index(Configuration.DEFAULT_MAIL_FIELDS[i + 1])
                client_job[Configuration.DEFAULT_MAIL_FIELDS[i]] = message[find_from: find_to - 1]
            except IndexError:
                find_from = message.index(Configuration.FINAL_ITEM) + 6
                find_to = len(message)
                client_job[Configuration.DEFAULT_MAIL_FIELDS[i]] = message[find_from: find_to]
            except ValueError:
                client_job[Configuration.DEFAULT_MAIL_FIELDS[i]] = 'N/A'
            except Exception as e:
                cls.logger.exception(f'Caught exception while running create_client_dictionary: {e}', message)

        client_job['Notes:'].replace('(Sent via KL Dental Services', '')
        estimated, normalized_job = etn.normalize_date_time(client_job)
        return estimated, normalized_job
