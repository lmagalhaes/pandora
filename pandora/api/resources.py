import logging

import falcon
from pandora.models import Company, Person
from sqlalchemy.orm import Session
import json


class BaseResource:

    routes = [
        '/'
    ]

    def __init__(self, api):
        self._api = api
        self._logger = logging.getLogger(self.__class__.__name__)
        self._logger.info("Creating Resource %s", self.__class__.__name__)
        self._set_routes()
        self.db_session: Session = self._api.db_session

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
        '/company/{id_company:int}/'
    ]

    def on_get(self, request, response, id_company):
        company: Company = self.db_session.query(Company).filter(Company.id == id_company).one_or_none()
        if company:
            response.body = json.dumps({'employees': [dict(employee) for employee in company.employees]})
        else:
            response.status = falcon.HTTP_404
            response.body = f'Company with id ({id_company}) not found'


class CommonFriendsResource(BaseResource):

    routes = [
        '/person/{id_person:int}/friends/{id_another_person:int}/'
    ]

    def on_get(self, request, response, id_person, id_another_person):

        person, another_person = self.db_session.query(Person).filter(
            Person.id.in_([id_person, id_another_person])
        ).all()

        commons_friends = [
            dict(friend)
            for friend in person.common_friends_with(another_person)
            if not self.filter_out(friend)
        ]

        response.body = json.dumps(dict(
            person1=dict(person),
            person2=dict(another_person),
            commons_friends=commons_friends
        ))

    def filter_out(person: Person) -> bool:
        return bool(person.has_died) or person.eye_color != 'brown'


class PersonResource(BaseResource):

    routes = [
        '/person/{id_person:int}/'
    ]

    def on_get(self, request, response, id_person, id_another_person=None):
        person = self.db_session.query(Person).filter(Person.id == id_person).one_or_none()
        if not person:
            response.status = falcon.HTTP_404
            response.body = f'Person with id ({id_person}) not found'
            return
        fruits = []
        vegetables = []
        for food in person.foods:
            if food.is_fruit:
                fruits.append(food.name)
            else:
                vegetables.append(food.name)
        response.body = json.dumps({'usename': person.name, 'age': person.age, 'fruits': fruits, 'vegetables': vegetables})
