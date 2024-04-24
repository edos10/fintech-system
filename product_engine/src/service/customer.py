from db.dao import *
from sqlalchemy import select
from models.model_orm import *


class CustomerRepository(BaseRepository):
    async def create(self, client: Clients):
        client = ClientCreate(**client.dict())
        self.session.add(client)
        await self.session.commit()

    async def get_by_id(self, product_code):
        result = await self.session.execute(select(Clients).where(Clients.id == product_code))
        return result.scalars().first()

    async def get_all(self):
        result = await self.session.execute(select(Clients))
        return result.scalars().all()

    async def delete_by_id(self, obj_id):
        existing_product = await self.session.execute(select(Clients).where(Clients.id == obj_id))
        if not existing_product:
            return
        db_product = existing_product.scalar_one()
        await self.session.delete(db_product)
        await self.session.commit()
