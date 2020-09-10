from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import EmailType, ScalarListType
from dictalchemy import DictableModel


Base: declarative_base = declarative_base(cls=DictableModel)


__company_table_name__ = 'company'
__food_table_name__ = 'food'
__person_relationship_table_name__ = 'person_relates_to_person'
__person_likes_food_table_name__ = 'person_likes_food'
__company_employs_person_table_name__ = 'company_employs_person'
__person_table_name__ = 'person'


class BaseModel:
    @classmethod
    def from_dict(cls, data):
        instance = cls()
        important_fields = {
            ''.join(column.key.lower().split('_')): column.key
            for column in instance.__table__.columns
        }

        for key, value in data.items():
            parsed_field = ''.join(key.lower().split('_'))
            if parsed_field in important_fields:
                setattr(instance, important_fields[parsed_field], value)
        return instance


class PersonRelatesToPerson(BaseModel, Base):
    __tablename__ = __person_relationship_table_name__

    person_id = Column(ForeignKey('person.id'), primary_key=True)
    friend_id = Column(ForeignKey('person.id'), primary_key=True)

    person = relationship(
        'Person',
        foreign_keys=[person_id],
        uselist=False
    )

    friend = relationship(
        'Person',
        foreign_keys=[friend_id],
        uselist=False
    )


class PersonLikesFood(BaseModel, Base):
    __tablename__ = __person_likes_food_table_name__

    person_id = Column(ForeignKey('person.id'), primary_key=True)
    food_id = Column(ForeignKey('food.id'), primary_key=True)


class CompanyEmploysPerson(Base):
    __tablename__ = __company_employs_person_table_name__

    company_id = Column(ForeignKey('company.id'), primary_key=True)
    person_id = Column(ForeignKey('person.id'), primary_key=True)


class Company(BaseModel, Base):
    __tablename__ = __company_table_name__

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)

    employees = relationship(
        'Person',
        secondary=__company_employs_person_table_name__,
        back_populates='companies'
    )


class Person(BaseModel, Base):
    __tablename__ = __person_table_name__

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    has_died = Column(Boolean, default=False)
    eye_color = Column(String(32))
    email = Column(EmailType)
    age = Column(Integer)
    phone = Column(String(20))
    address = Column(String(255))
    tags = Column(ScalarListType())

    foods = relationship(
        'Food',
        secondary=__person_likes_food_table_name__,
        back_populates='persons'
    )

    companies = relationship(
        'Company',
        secondary=__company_employs_person_table_name__,
        back_populates='employees'
    )

    person_friends = relationship(
        'PersonRelatesToPerson',
        primaryjoin=(id == PersonRelatesToPerson.__table__.c.person_id)
    )

    @property
    def friends(self):
        return [friend.friend for friend in self.person_friends]

    def common_friends_with(self, another_person):
        return set(self.friends).intersection(set(another_person.friends))


class Food(BaseModel, Base):
    __tablename__ = __food_table_name__

    id = Column(Integer, primary_key=True)
    name = Column(String(15), nullable=False, unique=True)
    is_fruit = Column(Boolean, default=False)

    persons = relationship(
        'Person',
        secondary=__person_likes_food_table_name__,
        back_populates='foods'
    )

