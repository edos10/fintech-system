from db.dao import *
from sqlalchemy import select
from models.model_orm import *

import random


class AgreementRepository(BaseRepository):
    async def create(self, request: CreditRequest):

        # надо пофиксить, чет не очень, погуглить бы
        # нерабочий вариант upd
        if not isinstance(request.birthday, str) \
            or not isinstance(request.term, int) \
            or not isinstance(request.product_code, str) \
            or not isinstance(request.disbursment_amount, int) \
            or not isinstance(request.interest, int) \
            or not isinstance(request.phone, str) \
            or not isinstance(request.email, str) \
            or not isinstance(request.first_name, str)\
            or not isinstance(request.second_name, str) \
            or not isinstance(request.third_name, str)\
            or not isinstance(request.passport_number, str)\
                or not isinstance(request.salary, int):
            raise ValueError("wrong input data")

        id_client = await self.session.execute(select(Clients.id))

        dict_for_client = request.dict()
        dict_for_client.pop('product_code')

        client = ClientCreate(surname=request.first_name,
                              name=request.second_name,
                              patronymic=request.third_name,
                              birth_date=datetime.datetime.strptime(request.birthday, '%d.%m.%Y'),
                              client_salary=request.salary,
                              passport=request.passport_number,
                              phone_number=request.phone,
                              id=len(id_client.scalars().all()) + 1)

        exists_res = await self.session.execute(select(Clients).where(
            Clients.client_salary == client.client_salary).where(Clients.surname == client.surname).where(
            client.name == Clients.name).where(Clients.patronymic == client.patronymic).where(
            client.phone_number == Clients.phone_number).where(Clients.passport == client.passport).where(
            client.birth_date == Clients.birth_date)
        )

        client_exists = exists_res.scalars().all()
        if not client_exists:
            current_client = Clients(**client.dict())
            self.session.add(current_client)
            await self.session.commit()
        else:
            current_client = client_exists[0]

        id_agr = await self.session.execute(select(Agreements.id))

        min_origination_amount = await self.session.execute(select(Products.min_origination_amount).where(
            Products.id == request.product_code))

        max_origination_amount = await self.session.execute(select(Products.max_origination_amount).where(
            Products.id == request.product_code))

        min_origination_amount = min_origination_amount.scalars().all()
        max_origination_amount = max_origination_amount.scalars().all()

        if not min_origination_amount:
            raise ValueError("wrong product code")

        current_product = await self.session.execute(select(Products).where(
            Products.id == request.product_code))

        current_product = current_product.scalars().first()

        if not (current_product.min_load_term <= request.term <= current_product.max_load_term) \
            or not (current_product.min_interest <= request.interest <= current_product.max_interest) \
            or not (current_product.min_principal_amount <= request.disbursment_amount <=
                    current_product.max_principal_amount):
            raise ValueError("wrong conditions for taking credit")

        new_origination = random.randint(min_origination_amount[0], max_origination_amount[0])
        new_id = len(id_agr.scalars().all()) + 1

        agreement = Agreements(
            id=new_id,
            name_product=request.product_code,
            id_client=current_client.id,
            term=request.term,
            interest=request.interest,
            principal=request.disbursment_amount + new_origination,
            contract_status="New",
            datetime_activation=datetime.datetime.now(),
            origination=new_origination)
        self.session.add(agreement)
        await self.session.commit()

        # возвращаю не только номер договора, но и id клиента и сумму кредита для удобства работы producer kafka
        return new_id, current_client.id, request.disbursment_amount

    async def get_by_id(self, agreement_id):
        result = await self.session.execute(select(Agreements).where(Agreements.id == agreement_id))
        return result.scalars().first()

    async def get_all_on_client_id(self, client_id: int):
        result = await self.session.execute(select(Agreements).where(Agreements.id_client == client_id))
        return result.scalars().all()
    
    async def return_id_client(self, client):
        exists_res = await self.session.execute(select(Clients).where(
            Clients.client_salary == client['client_salary']).where(Clients.surname == client['surname']).where(
            client['name'] == Clients.name).where(Clients.patronymic == client['patronymic']).where(
            client['phone_number'] == Clients.phone_number).where(Clients.passport == client['passport']).where(
            client['birth_date'] == Clients.birth_date)
        )

        id_client = -1
        client_exists = exists_res.scalars().all()
        if not client_exists:
            current_client = Clients(**client.dict())
            self.session.add(current_client)
            await self.session.commit()
        else:
            id_client = client_exists[0].id
        
        id_client = current_client.id
        return id_client

    async def delete_by_id(self, obj_id):
        existing_product = await self.session.execute(select(Agreements).where(Agreements.id == obj_id))
        db_product = existing_product.scalar()

        await self.session.delete(db_product)
        await self.session.commit()
