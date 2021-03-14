from threading import local
import traceback
import os
from datetime import datetime
from config.configuration import Configuration
from lib.logging.log_rotator import DailyLogRotationHandler

_tls = local()

def get_logger():
    logger = getattr(_tls, "logger", None)
    if not logger:
        logger = GabryelLogger(log_directory_path=Configuration.LOG_DIR_PATH,
                               debug_mode=Configuration.DEBUG_MODE)
        _tls.logger = logger

    return logger


class GabryelLogger:
    def __init__(self, log_directory_path=None, debug_mode=False):
        self.debug_mode = debug_mode
        self.log_filename = f"{datetime.now().strftime('%Y%m%d')}-gabryel-logs"
        self.log_directory_path = self._make_path_windows(log_directory_path)
        self.log_filepath = self.create_full_log_path()
        self.error_log_filepath = self.create_full_log_path(error=True)
        self.rotator = DailyLogRotationHandler(self)

    @classmethod
    def _make_path_windows(cls, log_directory_path):
        try:
            if not os.path.isdir(log_directory_path):
                os.mkdir(log_directory_path)
            return log_directory_path
        except Exception as e:
            cls._log_console_only(f'An exception occurred while trying to create the path: {e}')
            return

    def create_full_log_path(self, error=False):
        filename = f'{self.log_filename}-ERROR.log' if error else f'{self.log_filename}.log'
        return os.path.join(self.log_directory_path, filename) if self.log_directory_path else None

    @classmethod
    def _log_console_only(cls, msg, level='ERROR'):
        print(cls._build_message(msg, level))

    @classmethod
    def _build_message(cls, msg, level):
        return f'[{datetime.now().time()}][{level}] {msg}'

    def exception(self, msg, *calls):
        msg = self._build_message(msg, 'EXCEPTION')
        self._log(msg, *calls, err=True)

    def warning(self, msg):
        msg = self._build_message(msg, 'WARNING')
        self._log(msg)

    def info(self, msg):
        msg = self._build_message(msg, 'INFO')
        self._log(msg)

    def debug(self, msg):
        if self.debug_mode:
            msg = self._build_message(msg, 'DEBUG')
            self._log(msg)

    def _log(self, msg, *calls, err=False):
        if err:
            msg = f'{traceback.format_exc()}\n{msg}'
        if calls:
            msg += '\nCalled with:\n' + '\n'.join([str(x) for x in calls])

        print(msg)

        self.rotator.check_logfile()
        if self.log_filepath:
            with open(self.log_filepath, "a+") as logfile:
                logfile.write(msg + "\n")

        if err and self.error_log_filepath:
            with open(self.error_log_filepath, "a+") as logfile:
                logfile.write(msg + "\n")
