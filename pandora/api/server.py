import falcon
import logging

from pandora.settings import settings
from pandora.logs import configure
from .resources import WelcomeResource, CompanyResource, PersonResource

configure(
    debug=settings['debug']
)


class PandoraApi(falcon.API):
    def __init__(self, configs):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.debug('Starting Pandora Api')
        self.configs = configs


api = PandoraApi(configs=settings)
WelcomeResource(api=api)
CompanyResource(api=api)
PersonResource(api=api)
