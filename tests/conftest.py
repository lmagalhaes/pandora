import pytest
from falcon import Request, Response
from falcon.testing import create_environ
from unittest.mock import MagicMock

from pandora.models import Person


@pytest.fixture
def falcon_request():
    env = create_environ(query_string='')
    request = Request(env)
    return request


@pytest.fixture
def falcon_response():
    return Response()


@pytest.fixture
def db_session_mock():
    filter_mock = MagicMock(return_value=MagicMock())
    db_session_mock = MagicMock()
    db_session_mock.query.return_value = filter_mock
    return db_session_mock


def generate_person(id_, name):
    return Person.from_dict({
        "id": id_,
        "name": name,
        "has_died": False,
        "eye_color": "brown",
        "email": f"{name}@{name}.com",
        "age": 61,
        "phone": "+1 (910) 567-3630",
        "address": "628 Sumner Place",
        "tags": []
    })


def generate_mocked_relationship(person1, person2):
    mocked_relationship = MagicMock()
    mocked_relationship.person = person1
    mocked_relationship.friend = person2

    return mocked_relationship
