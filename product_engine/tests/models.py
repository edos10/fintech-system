import datetime

class Agreements():
    __tablename__ = 'contracts'
    id: int
    name_product: str
    id_client: int
    term: int
    principal: int
    interest: int
    origination: int
    datetime_activation: datetime.datetime
    contract_status: str
