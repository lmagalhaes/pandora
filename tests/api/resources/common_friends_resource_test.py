import json
from falcon import HTTP_404
from unittest.mock import MagicMock

from pandora.api.resources import CommonFriendsResource
from pandora.models import Person
from tests.conftest import generate_person, generate_mocked_relationship


class TestOnGet:

    def test_should_request_request_db_with_input_ids(self, falcon_request, falcon_response, db_session_mock):
        api_mock = MagicMock()
        api_mock.db_session = db_session_mock

        query_mock = db_session_mock.query()
        query_mock.filter.return_value.all.return_value = [Person(id=1)]

        ana_id, luca_id = 0, 1
        resource = CommonFriendsResource(api=api_mock)
        resource.on_get(falcon_request, falcon_response, ana_id, luca_id)

        query_mock.filter.assert_called_once()

        '''
        # the below is done this way due to a bug found on the _Call implementation
        # https://stackoverflow.com/questions/57636747/how-to-perform-assert-has-calls-for-a-getitem-call
        '''
        called_filter_input = query_mock.filter.call_args_list[0].__getitem__(0)[0]
        expected_filter_input = str(Person.id.in_([ana_id, luca_id]))
        assert expected_filter_input == str(called_filter_input)

    def test_return_404_if_one_of_the_ids_do_not_match_person(self, falcon_request, falcon_response, db_session_mock):
        api_mock = MagicMock()
        api_mock.db_session = db_session_mock

        query_mock = db_session_mock.query()
        query_mock.filter.return_value.all.return_value = [Person(id=1)]

        ana_id, luca_id = 0, 1
        resource = CommonFriendsResource(api=api_mock)
        resource.on_get(falcon_request, falcon_response, ana_id, luca_id)

        assert 'Person with id (0) not found' == falcon_response.body
        assert HTTP_404 == falcon_response.status

    def test_return_details_for_of_each_person(self, falcon_request, falcon_response, db_session_mock):
        ana_id, luca_id = 0, 1
        ana = generate_person(ana_id, 'ana')
        luca = generate_person(luca_id, 'luca')

        api_mock = MagicMock()
        api_mock.db_session = db_session_mock

        query_mock = db_session_mock.query()
        query_mock.filter.return_value.all.return_value = [ana, luca]

        resource = CommonFriendsResource(api=api_mock)
        resource.on_get(falcon_request, falcon_response, ana_id, luca_id)

        expected_response = json.dumps(dict(
            person1=dict(ana),
            person2=dict(luca),
            common_friends=[]
        ))

        assert expected_response == falcon_response.body

    def test_return_detailed_common_friends_list(self, falcon_request, falcon_response, db_session_mock):
        ana_id, luca_id = 0, 1
        ana = generate_person(ana_id, 'ana')
        luca = generate_person(luca_id, 'luca')

        marco = generate_person(3, 'marco')
        vanessa = generate_person(4, 'vanessa')
        carla = generate_person(5, 'carla')

        ana.personal_friends = [
            generate_mocked_relationship(ana, marco),
            generate_mocked_relationship(ana, vanessa),
        ]

        luca.personal_friends = [
            generate_mocked_relationship(ana, vanessa),
            generate_mocked_relationship(ana, carla),
        ]

        api_mock = MagicMock()
        api_mock.db_session = db_session_mock

        query_mock = db_session_mock.query()
        query_mock.filter.return_value.all.return_value = [ana, luca]

        resource = CommonFriendsResource(api=api_mock)
        resource.on_get(falcon_request, falcon_response, ana_id, luca_id)

        expected_response = json.dumps(dict(
            person1=dict(ana),
            person2=dict(luca),
            common_friends=[
                dict(vanessa)
            ]
        ))
        assert expected_response == falcon_response.body

    def test_return_detailed_common_friends_list_who_have_brown_eye_and_is_alive(
            self,
            falcon_request,
            falcon_response,
            db_session_mock
    ):
        ana_id, luca_id = 0, 1
        ana = generate_person(ana_id, 'ana')
        luca = generate_person(luca_id, 'luca')

        vanessa = generate_person(4, 'vanessa')

        marco = generate_person(3, 'marco')
        marco.eye_color = 'green'

        carla = generate_person(5, 'carla')
        carla.has_died = True

        ana.personal_friends = [
            generate_mocked_relationship(ana, marco),
            generate_mocked_relationship(ana, vanessa),
            generate_mocked_relationship(ana, carla),
        ]

        luca.personal_friends = [
            generate_mocked_relationship(ana, vanessa),
            generate_mocked_relationship(ana, carla),
        ]

        api_mock = MagicMock()
        api_mock.db_session = db_session_mock

        query_mock = db_session_mock.query()
        query_mock.filter.return_value.all.return_value = [ana, luca]

        resource = CommonFriendsResource(api=api_mock)
        resource.on_get(falcon_request, falcon_response, ana_id, luca_id)

        expected_response = json.dumps(dict(
            person1=dict(ana),
            person2=dict(luca),
            common_friends=[
                dict(vanessa)
            ]
        ))
        assert expected_response == falcon_response.body
