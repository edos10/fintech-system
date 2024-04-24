import datetime

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import TIMESTAMP
from pydantic import BaseModel
from db.base import Base


"""
исправить на mapped column, relationship(почитать про нее)
почитать про дженерики для базового класса dao
"""


class Agreements(Base):
    __tablename__ = 'contracts'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name_product = Column(String)
    id_client = Column(Integer)
    term = Column(Integer)
    principal = Column(Integer)
    interest = Column(Integer)
    origination = Column(Integer)
    datetime_activation = Column(TIMESTAMP)
    contract_status = Column(String)


class Payments(Base):
    __tablename__ = 'payments'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    plan_datetime = Column(TIMESTAMP)
    start_period = Column(TIMESTAMP)
    payment_for_base = Column(Integer)
    payment_for_percents = Column(Integer)
    number_payment = Column(Integer)
    payment_status = Column(String)


class Products(Base):
    __tablename__ = 'products'
    id = Column(String, primary_key=True)
    name_for_user = Column(String)
    min_load_term = Column(Integer)
    max_load_term = Column(Integer)
    min_principal_amount = Column(Integer)
    max_principal_amount = Column(Integer)
    min_interest = Column(Integer)
    max_interest = Column(Integer)
    min_origination_amount = Column(Integer)
    max_origination_amount = Column(Integer)


class Clients(Base):
    __tablename__ = 'clients'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    surname = Column(String)
    name = Column(String)
    patronymic = Column(String)
    phone_number = Column(String)
    passport = Column(String)
    client_salary = Column(Integer)
    birth_date = Column(TIMESTAMP)


class ProductCreate(BaseModel):
    max_load_term: int
    name_for_user: str
    max_principal_amount: int
    max_interest: float
    max_origination_amount: int
    min_principal_amount: int
    id: str
    min_load_term: int
    min_interest: float
    min_origination_amount: int


class AgreementCreate(BaseModel):
    id: int
    name_product: str
    id_client: int
    term: int
    principal: int
    interest: int
    origination: int
    datetime_activation: datetime.datetime
    contract_status: str


class ClientCreate(BaseModel):
    id: int
    surname: str
    name: str
    patronymic: str
    phone_number: str
    passport: str
    client_salary: int
    birth_date: datetime.datetime


class CreditRequest(BaseModel):
    product_code: str
    first_name: str
    second_name: str
    third_name: str
    birthday: str
    passport_number: str
    email: str
    phone: str
    salary: int
    term: int
    interest: int
    disbursment_amount: int
