import os.path
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from lib.logging.gabryel_logger import get_logger


class ServiceManager:
    _SCOPES = ['https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/calendar.events']

    _VERSIONS = {
        'gmail': 'v1',
        'calendar': 'v3'
    }

    logger = get_logger()

    @classmethod
    def get_service(cls, service_name):
        try:
            cls.logger.info(f'Getting services')
            if os.path.exists(f'creds/pickles/api_pickle_file.pickle'):
                cls.logger.debug(f'Found credential pickle for services.. Attempting to load')
                with open(f'creds/pickles/api_pickle_file.pickle', 'rb') as token:
                    creds = pickle.load(token)
            else:
                cls.logger.warning(f'No credential pickle found.')
                creds = None
            if not creds or not creds.valid:
                creds = cls.authorize_with_service()
                cls.logger.debug(f'Dumping credentials to pickle file creds/pickles/api_pickle_file.pickle.')
                with open(f'creds/pickles/api_pickle_file.pickle', 'wb') as token:
                    pickle.dump(creds, token)

            resource = build(service_name, cls._VERSIONS.get(service_name), credentials=creds)
            return resource
        except Exception as e:
            cls.logger.exception(f'Caught exception while attempting to build service: {e}')
            return None

    @classmethod
    def authorize_with_service(cls):
        cls.logger.debug(f'Attempting to authorize with creds/api_credentials.json')
        try:
            flow = InstalledAppFlow.from_client_secrets_file(f'creds/api_credentials.json', cls._SCOPES)
            return flow.run_local_server(port=0)
        except Exception as e:
            cls.logger.exception(f'Caught exception while attempting to authorize credentials: {e}')

    @classmethod
    def refresh_service(cls):
        cls.logger.info(f'Refreshing service')
        with open(f'creds/pickles/api_pickle_file.pickle', 'rb') as token:
            creds = pickle.load(token)
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                cls.logger.info(f'Refreshed service successfully.')
            else:
                cls.logger.warning(f'Could not refresh service.')
                cls.logger.debug(f'Expired: {creds.expired} | Has refresh token: {creds.refresh_token}')
