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
    __tablename__ = 'person_friends'

    person_id = Column(ForeignKey('persons.id'), primary_key=True)
    friend_id = Column(ForeignKey('persons.id'), primary_key=True)

    person = relationship("Person", foreign_keys=[person_id], uselist=False)
    friend = relationship("Person", foreign_keys=[friend_id], uselist=False)


class PersonLikesFood(BaseModel, Base):
    __tablename__ = 'person_foods'

    person_id = Column(ForeignKey('persons.id'), primary_key=True)
    food_id = Column(ForeignKey('foods.id'), primary_key=True)


class CompanyEmploysPerson(Base):
    __tablename__ = 'company_employees'

    company_id = Column(ForeignKey('companies.id'), primary_key=True)
    person_id = Column(ForeignKey('persons.id'), primary_key=True)


class Company(BaseModel, Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)

    employees = relationship('Person', secondary=CompanyEmploysPerson.__tablename__, back_populates=__tablename__)


class Person(BaseModel, Base):
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

    foods = relationship('Food', secondary=PersonLikesFood.__tablename__, back_populates=__tablename__)

    companies = relationship('Company', secondary=CompanyEmploysPerson.__tablename__, back_populates='employees')

    friends = relationship('PersonRelatesToPerson', primaryjoin=(id == PersonRelatesToPerson.__table__.c.person_id))


class Food(BaseModel, Base):
    __tablename__ = 'foods'

    id = Column(Integer, primary_key=True)
    name = Column(String(15), nullable=False, unique=True)
    is_fruit = Column(Boolean, default=False)

    persons = relationship('Person', secondary=PersonLikesFood.__tablename__, back_populates=__tablename__)


#
# class BaseModel:
#     @classmethod
#     def from_dict(cls, data):
#         instance = cls()
#         important_fields = {
#             ''.join(column.key.lower().split('_')): column.key
#             for column in instance.__table__.columns
#         }
#
#         for key, value in data.items():
#             parsed_field = ''.join(key.lower().split('_'))
#             if parsed_field in important_fields:
#                 setattr(instance, important_fields[parsed_field], value)
#         return instance
#
#
# class PersonRelatesToPerson(BaseModel, Base):
#     __tablename__ = __person_relationship_table_name__
#
#     person_id = Column(ForeignKey('person.id'), primary_key=True)
#     friend_id = Column(ForeignKey('person.id'), primary_key=True)
#
#     person = relationship(__person_table_name__, foreign_keys=[person_id], uselist=False)
#     friend = relationship(__person_table_name__, foreign_keys=[friend_id], uselist=False)
#
#
# class PersonLikesFood(BaseModel, Base):
#     __tablename__ = __person_likes_food_table_name__
#
#     person_id = Column(ForeignKey('person.id'), primary_key=True)
#     food_id = Column(ForeignKey('food.id'), primary_key=True)
#
#
# class CompanyEmploysPerson(Base):
#     __tablename__ = __company_employs_person_table_name__
#
#     company_id = Column(ForeignKey('company.id'), primary_key=True)
#     person_id = Column(ForeignKey('person.id'), primary_key=True)
#
#
# class Company(BaseModel, Base):
#     __tablename__ = __company_table_name__
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(32), unique=True)
#
#     employees = relationship(
#         'Person',
#         secondary=__company_employs_person_table_name__,
#         back_populates=__tablename__
#     )
#
#
# class Person(BaseModel, Base):
#     __tablename__ = __person_table_name__
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(32), nullable=False)
#     has_died = Column(Boolean, default=False)
#     eye_color = Column(String(32))
#     email = Column(EmailType)
#     age = Column(Integer)
#     phone = Column(String(20))
#     address = Column(String(255))
#     tags = Column(ScalarListType())
#
#     foods = relationship(
#         __food_table_name__,
#         secondary=__person_likes_food_table_name__,
#         back_populates=__tablename__
#     )
#
#     companies = relationship(
#         __company_table_name__,
#         secondary=__company_employs_person_table_name__,
#         back_populates='employees'
#     )
#
#     friends = relationship(
#         __person_relationship_table_name__,
#         primaryjoin=(id == PersonRelatesToPerson.__table__.c.person_id)
#     )
#
#
# class Food(BaseModel, Base):
#     __tablename__ = __food_table_name__
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String(15), nullable=False, unique=True)
#     is_fruit = Column(Boolean, default=False)
#
#     person = relationship(
#         __person_table_name__,
#         secondary=__person_likes_food_table_name__,
#         back_populates=__tablename__
#     )
