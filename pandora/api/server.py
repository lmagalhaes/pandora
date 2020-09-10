import falcon
import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from pandora import settings
from pandora.logs import configure
from .resources import WelcomeResource, CompanyResource, PersonResource, CommonFriendsResource


configure(debug=settings.DEBUG)


class PandoraApi(falcon.API):

    def __init__(self, configs: settings):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug('Starting Pandora Api')
        self.configs: settings = configs
        self.db_session = self.create_db_session()

    def create_db_session(self):
        self.logger.debug('Creating DB session')
        engine = create_engine(self.configs.SQLALCHEMY_URI)
        # engine = create_engine(self.configs.SQLALCHEMY_URI, echo=self.configs.DEBUG)
        return Session(bind=engine)


api = PandoraApi(configs=settings)
WelcomeResource(api=api)
CompanyResource(api=api)
PersonResource(api=api)
CommonFriendsResource(api=api)


