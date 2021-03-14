from datetime import datetime, timedelta
from config.configuration import Configuration
from lib.logging.gabryel_logger import get_logger


class EventTimeNormalizer:
    logger = get_logger()

    @classmethod
    def fit_in_worktime(cls, time):
        opening_hours = datetime.strptime('8:30:0', '%H:%M:%S')
        closing_hours = datetime.strptime('18:0:0', '%H:%M:%S')
        cls.logger.debug(f'Fitting in worktime with: {time}')
        try:
            if time.time() < opening_hours.time():
                return opening_hours

            if time.time() > closing_hours.time():
                return closing_hours

            return time

        except Exception as e:
            cls.logger.exception(f'Encountered exception in fit_in_worktime: {e}', time)
            return None

    @classmethod
    def appoint_aprox_job_duration(cls, job):
        for i in Configuration.JOB_DURATIONS.keys():
            if i in job:
                return_date = datetime.now() + timedelta(days=Configuration.JOB_DURATIONS.get(i))
                return datetime.strftime(return_date, '%d/%m/%Y')

    @classmethod
    def no_datetime_found(cls, event_dict):
        if event_dict.get('Pickup Date:') in Configuration.BAD_INPUT:
            event_dict['Pickup Date:'] = datetime.strftime(datetime.now(), '%d/%m/%Y')
        if event_dict.get('Pickup Time:') in Configuration.BAD_INPUT:
            event_dict['Pickup Time:'] = datetime.strftime(datetime.now().replace(microsecond=0), '%I:%M:%S %p')
        if event_dict.get('Return Date:') in Configuration.BAD_INPUT:
            event_dict['Return Date:'] = cls.appoint_aprox_job_duration(event_dict['Job Type:'])
        if event_dict.get('Return Time:') in Configuration.BAD_INPUT:
            event_dict['Return Time:'] = datetime.strftime(datetime.now().replace(microsecond=0), '%I:%M:%S %p')
        return event_dict

    @classmethod
    def set_time(cls, date, time):
        cls.logger.info(f'Setting date and time for: {date.date(), time.time()}')
        try:
            datte = date.date().strftime("%Y-%m-%d")
            cls.logger.debug(f'Outcome: {datte} {time}')
            return datte, time.strftime("%H:%M:%S")
        except Exception as e:
            cls.logger.exception(f'Encountered exception in set_time: {e}', date, time)
            return None, None

    @classmethod
    def check_if_date_is_business_day(cls, date_to_check):
        cls.logger.debug(f'Checking for business day with: {date_to_check}')
        try:
            weekday = date_to_check.weekday()
            while weekday in (5, 6):
                date_to_check -= timedelta(days=1)
                cls.logger.debug(f'Current date: {date_to_check}')
                weekday = date_to_check.weekday()

            return date_to_check
        except Exception as e:
            cls.logger.exception(f'Encountered exception in check_if_date_is_business_day: {e}', date_to_check)
            return None

    @classmethod
    def create_one_hour_gap(cls, time, start):
        cls.logger.debug(f'Creating one hour gap with: {time, start}')
        try:
            new_time = time - timedelta(hours=1) if start else time + timedelta(hours=1)
            return cls.fit_in_worktime(new_time) if start else new_time
        except Exception as e:
            cls.logger.exception(f'Encountered exception in create_one_hour_gap: {e}', time)
            return

    @classmethod
    def set_starting_time(cls, t):
        try:
            return cls.create_one_hour_gap(datetime.strptime(t, "%I:%M:%S %p"), True)
        except ValueError:
            return cls.create_one_hour_gap(datetime.strptime(t, "%H:%M:%S %p"), True)
        except Exception as e:
            cls.logger.exception(f'Caught exception in normalize_date_time %I:%M:%S %p: {e}', t)
            return

    @classmethod
    def normalize_date_time(cls, client_job):
        cls.logger.info('Normalizing date-time for job')
        try:
            bad_input = False
            for k, v in client_job.items():
                if v in Configuration.BAD_INPUT:
                    cls.logger.debug(f'Bad input found: {k}')
                    client_job = cls.no_datetime_found(client_job)
                    bad_input = True

            pickup_time_start = cls.set_starting_time(client_job.get('Pickup Time:'))
            return_time_start = cls.set_starting_time(client_job.get('Return Time:'))

            pickup_date_end = datetime.strptime(client_job.get('Pickup Date:'), "%d/%m/%Y")
            pickup_date_end = cls.check_if_date_is_business_day(pickup_date_end)
            return_date_end = datetime.strptime(client_job.get('Return Date:'), "%d/%m/%Y")
            return_date_end = cls.check_if_date_is_business_day(return_date_end)

            pickup_time_end = cls.create_one_hour_gap(pickup_time_start, False)
            return_time_end = cls.create_one_hour_gap(return_time_start, False)
            client_job['Pickup Date:'], client_job['Pickup Time:'] = cls.set_time(pickup_date_end,
                                                                                  pickup_time_start)
            client_job['Return Date:'], client_job['Return Time:'] = cls.set_time(return_date_end,
                                                                                  return_time_start)

            client_job['Pickup Date End:'], client_job['Pickup Time End:'] = cls.set_time(pickup_date_end,
                                                                                          pickup_time_end)
            client_job['Return Date End:'], client_job['Return Time End:'] = cls.set_time(return_date_end,
                                                                                          return_time_end)
            return client_job, bad_input
        except Exception as e:
            cls.logger.exception(f'Caught exception in normalize_date_time: {e}', client_job)
            return None
