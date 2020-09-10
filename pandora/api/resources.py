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


class WelcomeResource(BaseResource):
    def on_get(self, request, response):
        response.body = 'Welcome to Pandora Api'


class CompanyResource(BaseResource):

    routes = [
        '/company/{id_company:int}/'
    ]

    def on_get(self, request, response, id_company):
        company = self.db_session.query(Company).filter(Company.id == id_company).one_or_none()
        if not company:
            response.status = falcon.HTTP_404
            response.body = f'Company with id ({id_company}) not found'
            return

        employees = [dict(employee) for employee in company.employees]
        response.body = json.dumps(dict(**dict(company), employees=employees))


class PersonResource(BaseResource):

    routes = [
        '/person/{id_person:int}/'
    ]

    def on_get(self, request, response, id_person):
        person = self.db_session.query(Person).filter(Person.id == id_person).one_or_none()
        if not person:
            response.status = falcon.HTTP_404
            response.body = f'Person with id ({id_person}) not found'
            return

        fruits, vegetables = self.separete_fruits_from_vegetables(person.foods)
        response.body = json.dumps(dict(username=person.name, age=person.age, fruits=fruits, vegetables=vegetables))

    def separete_fruits_from_vegetables(self, foods):
        fruits = []
        vegetables = []
        for food in foods:
            if food.is_fruit:
                fruits.append(food.name)
            else:
                vegetables.append(food.name)
        return fruits, vegetables


class CommonFriendsResource(BaseResource):

    routes = [
        '/person/{id_person:int}/common-friends/{id_another_person:int}/'
    ]

    def on_get(self, request, response, id_person, id_another_person):
        filter_ = Person.id.in_([id_person, id_another_person])
        people = self.db_session.query(Person).filter(filter_).all()

        if len(people) != 2:
            missing_id = id_person if people[0].id == id_another_person else id_another_person
            response.body = 'Person with id ({}) not found'.format(missing_id)
            response.status = falcon.HTTP_404
            return

        person, another_person = people
        commons_friends = [
            dict(friend)
            for friend in person.common_friends_with(another_person)
            if self.filter_in(friend)
        ]

        response.body = json.dumps(dict(
            person1=dict(person),
            person2=dict(another_person),
            common_friends=commons_friends
        ))

    def filter_in(self, person):
        return not bool(person.has_died) and person.eye_color == 'brown'

