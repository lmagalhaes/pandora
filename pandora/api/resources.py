import logging


class BaseResource:

    routes = [
        '/'
    ]

    def __init__(self, api):
        self._api = api
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info("Creating Resource %s", self.__class__.__name__)
        self._set_routes()

    def _set_routes(self):
        self._logger.info("Setting routes")
        for route in self.routes:
            self._api.add_route(route, self)

    def get_configs(self):
        return self._api.configs


class WelcomeResource(BaseResource):
    def on_get(self, request, response):
        response.body = 'Welcome to Pandora Api'


class CompanyResource(BaseResource):

    routes = [
        '/company'
    ]

    def on_get(self, request, response):
        response.body = 'Yet to be implemented'


class PersonResource(BaseResource):

    routes = [
        '/person'
    ]

    def on_get(self, request, response):
        response.body = 'Yet to be implemented'
