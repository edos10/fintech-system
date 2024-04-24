import datetime

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import TIMESTAMP
from pydantic import BaseModel
from common.base import Base


class Applications(Base):
    __tablename__ = 'applications'
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    # agreeement_id = Column(Integer)
    product_name = Column(String)
    status = Column(String)
    first_name = Column(String)
    second_name = Column(String)
    third_name = Column(String)
    birthday = Column(String)
    passport_number = Column(String)
    email = Column(String)
    phone = Column(String)
    salary = Column(Integer)
    term = Column(Integer)
    interest = Column(Integer)
    disbursment_amount = Column(Integer)


class ApplicationCreate(BaseModel):
    product_name: str
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
