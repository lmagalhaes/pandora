from pandora.api.server import api
from sqlalchemy.orm import Session


def test_api_initilialises_sql_alchemy_session():
    assert isinstance(api.db_session, Session)


