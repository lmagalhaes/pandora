from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import EmailType, ScalarListType


Base: declarative_base = declarative_base()


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


class PersonFriends(BaseModel, Base):
    __tablename__ = 'person_friends'

    person_id = Column(ForeignKey('persons.id'), primary_key=True)
    friend_id = Column(ForeignKey('persons.id'), primary_key=True)

    person = relationship("Persons", foreign_keys=[person_id], uselist=False)
    friend = relationship("Persons", foreign_keys=[friend_id], uselist=False)


class PersonFood(BaseModel, Base):
    __tablename__ = 'person_foods'

    person_id = Column(ForeignKey('persons.id'), primary_key=True)
    food_id = Column(ForeignKey('foods.id'), primary_key=True)


class CompanyEmployees(Base):
    __tablename__ = 'company_employees'

    company_id = Column(ForeignKey('companies.id'), primary_key=True)
    person_id = Column(ForeignKey('persons.id'), primary_key=True)


class Companies(BaseModel, Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)

    employees = relationship('Persons', secondary=CompanyEmployees.__tablename__, back_populates=__tablename__)


class Persons(BaseModel, Base):
    __tablename__ = 'persons'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)
    has_died = Column(Boolean, default=False)
    eye_color = Column(String(32))
    email = Column(EmailType)
    age = Column(Integer)
    phone = Column(String(20))
    address = Column(String(255))
    tags = Column(ScalarListType())

    foods = relationship('Foods', secondary=PersonFood.__tablename__, back_populates=__tablename__)

    companies = relationship('Companies', secondary=CompanyEmployees.__tablename__, back_populates='employees')

    friends = relationship('PersonFriends', primaryjoin=(id == PersonFriends.__table__.c.person_id))

    # friends = relationship('PersonFriends', primaryjoin=(id == PersonFriends.__table__.c.friend_id))


class Foods(BaseModel, Base):
    __tablename__ = 'foods'

    id = Column(Integer, primary_key=True)
    name = Column(String(15), nullable=False, unique=True)
    is_fruit = Column(Boolean, default=False)

    persons = relationship('Persons', secondary=PersonFood.__tablename__, back_populates=__tablename__)
