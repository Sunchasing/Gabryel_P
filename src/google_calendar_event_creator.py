from lib.logging.gabryel_logger import get_logger
from src.service_manager import ServiceManager
from config.configuration import Configuration

class GoogleCalendarHandler:
    logger = get_logger()

    _SVC = ServiceManager.get_service('calendar').events()

    @staticmethod
    def create_event_description(event_dict):
        event_description = ''
        for k, v in event_dict.items():
            event_description += f"{k} {v}\n"
        return event_description

    @classmethod
    def create_event(cls, estimated, event_dict, original_message):
        cls.logger.info('Creating Event...')
        pickup_event = cls._build_pickup_event(estimated, event_dict)
        dropoff_event = cls._build_dropoff_event(estimated, event_dict)
        try:
            cls._SVC.insert(calendarId='primary', body=pickup_event).execute()
            cls._SVC.insert(calendarId='primary', body=dropoff_event).execute()
        except Exception as e:
            try:
                ServiceManager.refresh_service()
            except: ...
            cls.logger.exception(f'Exception caught in create_event: {e}', event_dict, original_message)

    @classmethod
    def check_for_existing_job(cls, job):
        for key in Configuration.JOB_COLOURS.keys():
            if key in job:
                return key
        return 'Unspecified'

    @classmethod
    def _build_pickup_event(cls, estimated, event_dict):

        tag = '[Est. P]' if estimated else '[P]'

        event_description = cls.create_event_description(event_dict)
        colour = Configuration.JOB_COLOURS.get('Pickup')[0]
        if event_dict['Patient Name:'] == 'N/A' or not event_dict['Patient Name:']:
            event_dict['Patient Name:'] = 'Unspecified'
        event_dict['Job Type:'] = cls.check_for_existing_job(event_dict.get('Job Type:'))
        pickup_event = {
            "kind": "calendar#calendar",
            'summary': f'{tag} {event_dict.get("Job Type:")} - {event_dict.get("Patient Name:")}',
            'colorId': f'{colour}',
            'location': f'{event_dict.get("Address or Business Name:")}',
            'description': event_description,
            'start': {
                'dateTime': f'{event_dict.get("Pickup Date:")}T{event_dict.get("Pickup Time:")}',
                'timeZone': 'Australia/Brisbane',
            },
            'end': {
                'dateTime': f'{event_dict.get("Pickup Date End:")}T{event_dict.get("Pickup Time End:")}',
                'timeZone': 'Australia/Brisbane',
            },
        }
        cls.logger.info(f'Created pickup event {pickup_event.get("summary")} for '
                        f'{(pickup_event.get("start").get("dateTime")).replace("T", " ")}')
        return pickup_event

    @classmethod
    def _build_dropoff_event(cls, estimated, event_dict):

        tag = '[Est. D]' if estimated else '[D]'

        event_description = cls.create_event_description(event_dict)
        colour = Configuration.JOB_COLOURS.get('Other')[0]

        for key, value in Configuration.JOB_COLOURS.items():
            if key in event_dict.get('Job Type:'):
                colour = value[0]

        event_dict['Job Type:'] = cls.check_for_existing_job(event_dict.get('Job Type:'))
        if event_dict['Patient Name:'] == 'N/A' or not event_dict['Patient Name:']:
            event_dict['Patient Name:'] = 'Unspecified'

        dropoff_event = {
            "kind": "calendar#calendar",
            'summary': f'{tag} {event_dict.get("Job Type:")} - {event_dict.get("Patient Name:")}',
            'colorId': f'{colour}',
            'location': f'{event_dict.get("Address or Business Name:")}',
            'description': event_description,
            'start': {
                'dateTime': f'{event_dict.get("Return Date:")}T{event_dict.get("Return Time:")}',
                'timeZone': 'Australia/Brisbane',
            },
            'end': {
                'dateTime': f'{event_dict.get("Return Date:")}T{event_dict.get("Return Time End:")}',
                'timeZone': 'Australia/Brisbane',
            },
        }
        cls.logger.info(f'Created dropoff event {dropoff_event.get("summary")} for '
                        f'{(dropoff_event.get("start").get("dateTime")).replace("T", " ")}')
        return dropoff_event
