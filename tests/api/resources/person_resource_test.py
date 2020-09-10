import json
from falcon import HTTP_404
from unittest.mock import MagicMock

from pandora.api.resources import PersonResource
from pandora.models import Person, Food
from tests.conftest import generate_person


class TestOnGet:

    def test_should_request_request_db_with_person_id(self, falcon_request, falcon_response, db_session_mock):
        api_mock = MagicMock()
        api_mock.db_session = db_session_mock

        query_mock = db_session_mock.query()
        query_mock.filter.return_value.one_or_none.return_value = Person(id=1)

        resource = PersonResource(api=api_mock)
        resource.on_get(falcon_request, falcon_response, 1)

        query_mock.filter.assert_called_once()

        '''
        # the below is done this way due to a bug found on the _Call implementation
        # https://stackoverflow.com/questions/57636747/how-to-perform-assert-has-calls-for-a-getitem-call
        '''
        called_filter_input = query_mock.filter.call_args_list[0].__getitem__(0)[0]
        expected_filter_input = str(Person.id == 1)
        assert expected_filter_input == str(called_filter_input)

    def test_return_404_if_person_is_not_found(self, falcon_request, falcon_response, db_session_mock):
        api_mock = MagicMock()
        api_mock.db_session = db_session_mock

        query_mock = db_session_mock.query()
        query_mock.filter.return_value.one_or_none.return_value = None

        resource = PersonResource(api=api_mock)
        resource.on_get(falcon_request, falcon_response, 0)

        assert 'Person with id (0) not found' == falcon_response.body
        assert HTTP_404 == falcon_response.status

    def test_return_details_for_of_each_person(self, falcon_request, falcon_response, db_session_mock):
        ana_id = 1
        ana = generate_person(ana_id, 'ana')

        api_mock = MagicMock()
        api_mock.db_session = db_session_mock

        query_mock = db_session_mock.query()
        query_mock.filter.return_value.one_or_none.return_value = ana

        resource = PersonResource(api=api_mock)
        resource.on_get(falcon_request, falcon_response, ana_id)

        expected_response = json.dumps(dict(
            username=ana.name,
            age=ana.age,
            fruits=[],
            vegetables=[]
        ))
        assert expected_response == falcon_response.body

    def test_return_details_with_food_sorted_between_fruits_and_vegetables(
            self,
            falcon_request,
            falcon_response,
            db_session_mock
    ):
        foods = [
            Food(id=1, name='apple', is_fruit=True),
            Food(id=1, name='cucumber', is_fruit=False)
        ]

        ana_id = 1
        ana = generate_person(ana_id, 'ana')
        ana.foods = foods

        api_mock = MagicMock()
        api_mock.db_session = db_session_mock

        query_mock = db_session_mock.query()
        query_mock.filter.return_value.one_or_none.return_value = ana

        resource = PersonResource(api=api_mock)
        resource.on_get(falcon_request, falcon_response, ana_id)

        expected_response = json.dumps(dict(
            username=ana.name,
            age=ana.age,
            fruits=[foods[0].name],
            vegetables=[foods[1].name]
        ))

        assert expected_response == falcon_response.body
