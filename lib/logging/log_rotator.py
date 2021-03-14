from datetime import datetime

class DailyLogRotationHandler:

    def __init__(self, logger):

        self.logger = logger

    def check_logfile(self):

        correct_log_name = f"{datetime.now().strftime('%Y%m%d')}-gabryel-logs"
        if correct_log_name != self.logger.log_filename:
            self.logger.log_filename = correct_log_name
            self.logger.log_filepath = self.logger.create_full_log_path()
            self.logger.error_log_filepath = self.logger.create_full_log_path(error=True)
