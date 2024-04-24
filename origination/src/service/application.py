from db.dao import *
from sqlalchemy import select, update
from models.model_orm import *
from config.config import *


class ApplicationRepository(BaseRepository):

    async def create(self, application: ApplicationCreate):

        """
        Create new application and add to DB
        :param application: request application data
        :return: None, if will not create application, will generate exception
        """
        exists_res = await self.session.execute(select(Applications).where(
            Applications.term == application.term).where(
            Applications.interest == application.interest).where(
            Applications.phone == application.phone).where(
            Applications.birthday == application.birthday).where(
            Applications.salary == application.salary).where(
            Applications.product_name == application.product_name).where(
            Applications.first_name == application.first_name).where(
            Applications.second_name == application.second_name).where(
            Applications.third_name == application.third_name).where(
            Applications.passport_number == application.passport_number).where(
            Applications.email == application.email).where(
            Applications.disbursment_amount == application.disbursment_amount))
        res = exists_res.scalars().first()
        if res:
            # надо поменять статус заявки на закрытую и убрать agreement_id, если он есть
            # а также скорее всего списать деньги со счета клиента, если они были перечислены
            id_for_close = res.id
            await self.update_status(id_for_close, "closed")
            raise ValueError("this application will close because of double-send, sorry")
        
        appl = Applications(**application.dict())
        appl.status = "new"
        self.session.add(appl)
        await self.session.commit()
        
        total_records = await self.session.execute(select(Applications))
        appl_id = len(total_records.scalars().all())
        
        return appl_id

    async def update_status(self, application_id: int, status: str):
        """
        Change status to definite from parameters
        :param application_id: input id integer
        :param status: required status for update in format string
        :return: None, if update unsuccessfully - exception will generate in route
        """
        result = await self.session.execute(select(Applications).where(Applications.id == application_id))
        if not result.scalars().first():
            raise ValueError("such application doesn't exists")
        
        await self.session.execute(update(Applications).where(Applications.id == application_id).values({'status': status}))
        await self.session.commit()
