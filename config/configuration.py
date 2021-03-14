class LoggerConfig:
    LOG_DIR_PATH = r"C:\ProgramData\Gabryel"  # Setting to None will revert to the default
    DEBUG_MODE = True  # Setting this to true will show the detailed debug logs. Fills up the disk quicker

class MailConfig:
    SENDER_EMAIL = 'my@milkshake.yard'  # sender e-mail to look for
    DEFAULT_MESSAGE_BEGINNING = 'Address or Business Name:'
    DEFAULT_MESSAGE_ENDING = r'buy'  # end of message
    FINAL_ITEM = 'Notes:'
    DEFAULT_MAIL_FIELDS = ['Address or Business Name:',
                           'Email Address:',
                           'Patient Name:',
                           'Pickup Date:',
                           'Pickup Time:',
                           'Job Type:',
                           'Return Date:',
                           'Return Time:',
                           'Notes:']

class JobsConfig:
    JOB_DURATIONS = {'Repair/Addition': 1,
                     'Reline': 1,
                     'Special Tray': 2,
                     'Try-In': 6,
                     'Denture': 6,
                     'Chrome Denture': 10,
                     'Crown & Bridge': 8,
                     'Bite Block': 5,
                     'Diagnostic Waxup': 7,
                     'Mouthguard': 4,
                     'Splint': 5,
                     'Retainer': 4,
                     'Orthodontic': 10,
                     'Other': 2}

    JOB_COLOURS = {'Repair/Addition': (11, 'Tomato'),
                   'Reline': (11, 'Tomato'),
                   'Try-In': (7, 'Peacock'),
                   'Denture': (9, 'Blueberry'),
                   'Chrome Denture': (1, 'Lavender'),
                   'Crown & Bridge': (5, 'Banana'),
                   'Special Tray': (3, 'Grape'),
                   'Mouthguard': (3, 'Grape'),
                   'Splint': (3, 'Grape'),
                   'Retainer': (3, 'Grape'),
                   'Orthodontic': (4, 'Flamingo'),
                   'Other': (11, 'Tomato'),
                   'Bite Block': (11, 'Tomato'),
                   'Diagnostic Waxup': (11, 'Tomato'),
                   'Pickup': (10, 'Basil')}


class Configuration(LoggerConfig, MailConfig, JobsConfig):
    BAD_INPUT = (' ', 'N/A', '', None)
    CYCLE_RATE = 60
