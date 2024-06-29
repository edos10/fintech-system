from db.dao import *
from sqlalchemy import select
from models.model_orm import *


class ProductRepository(BaseRepository):

    async def create(self, product: Products) -> bool:
        exists_res = await self.session.execute(select(Products).where(Products.id == product.id))
        if exists_res.scalar():
            return False
        db_product = Products(**product.dict())
        self.session.add(db_product)
        await self.session.commit()
        return True

    async def get_by_id(self, product_code):
        result = await self.session.execute(select(Products).where(Products.id == product_code))
        if not result.scalars():
            return None
        return result.scalars().first()

    async def get_all(self):
        result = await self.session.execute(select(Products))
        return result.scalars().all()

    async def delete_by_id(self, obj_id):
        existing_product = await self.session.execute(select(Products).where(Products.id == obj_id))
        db_product = existing_product.scalar()
        if not db_product:
            raise ValueError("Product with this code don't exists")
        await self.session.delete(db_product)
        await self.session.commit()
    
    async def return_id_client(self, data):
        pass
    
    async def get_all_on_client_id(self, obj_id) -> list:
        pass
