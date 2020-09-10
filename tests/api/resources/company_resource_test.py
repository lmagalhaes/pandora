import json
from falcon import HTTP_404
from unittest.mock import MagicMock

from pandora.api.resources import CompanyResource
from pandora.models import Company
from tests.conftest import generate_person


class TestOnGet:

    def test_should_request_db_with_company_id(self, falcon_request, falcon_response, db_session_mock):
        api_mock = MagicMock()
        api_mock.db_session = db_session_mock

        query_mock = db_session_mock.query()

        query_mock.filter.return_value.one_or_none.return_value = Company(id=1)

        resource = CompanyResource(api=api_mock)
        resource.on_get(falcon_request, falcon_response, 1)

        query_mock.filter.assert_called_once()

        '''
        # the below is done this way due to a bug found on the _Call implementation
        # https://stackoverflow.com/questions/57636747/how-to-perform-assert-has-calls-for-a-getitem-call
        '''
        called_filter_input = query_mock.filter.call_args_list[0].__getitem__(0)[0]
        expected_filter_input = str(Company.id == 1)
        assert expected_filter_input == str(called_filter_input)

    def test_return_404_if_company_is_not_found(self, falcon_request, falcon_response, db_session_mock):
        api_mock = MagicMock()
        api_mock.db_session = db_session_mock

        query_mock = db_session_mock.query()
        query_mock.filter.return_value.one_or_none.return_value = None

        resource = CompanyResource(api=api_mock)
        resource.on_get(falcon_request, falcon_response, 0)

        assert 'Company with id (0) not found' == falcon_response.body
        assert HTTP_404 == falcon_response.status

    def test_return_company_details(self, falcon_request, falcon_response, db_session_mock):
        company_id = 1
        company = Company(id=company_id, name='ACME', employees=[])

        api_mock = MagicMock()
        api_mock.db_session = db_session_mock

        query_mock = db_session_mock.query()
        query_mock.filter.return_value.one_or_none.return_value = company

        resource = CompanyResource(api=api_mock)
        resource.on_get(falcon_request, falcon_response, company_id)

        expected_response = json.dumps(dict(
            id=company.id,
            name=company.name,
            employees=company.employees
        ))
        assert expected_response == falcon_response.body

    def test_return_details_with_list_of_employees(
            self,
            falcon_request,
            falcon_response,
            db_session_mock
    ):
        company_id = 1
        employees = [
            generate_person(1, 'ana'),
            generate_person(2, 'pedro'),
            generate_person(3, 'rafael'),
        ]
        company = Company(id=company_id, name='ACME', employees=employees)

        api_mock = MagicMock()
        api_mock.db_session = db_session_mock

        query_mock = db_session_mock.query()
        query_mock.filter.return_value.one_or_none.return_value = company

        resource = CompanyResource(api=api_mock)
        resource.on_get(falcon_request, falcon_response, company_id)

        expected_response = json.dumps(dict(
            id=company.id,
            name=company.name,
            employees=[dict(employees) for employees in company.employees]
        ))
        assert expected_response == falcon_response.body
