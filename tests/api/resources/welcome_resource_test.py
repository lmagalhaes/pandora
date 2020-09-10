from unittest.mock import MagicMock

from pandora.api.resources import WelcomeResource


class TestOnGet:

    def test_returns_welcome_message(self, falcon_request, falcon_response):

        resource = WelcomeResource(api=MagicMock())
        resource.on_get(falcon_request, falcon_response)

        assert 'Welcome to Pandora Api' == falcon_response.body
