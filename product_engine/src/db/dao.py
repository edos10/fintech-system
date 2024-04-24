from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(ABC):
    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def create(self, obj):
        raise NotImplementedError

    @abstractmethod
    async def get_all_on_client_id(self, obj_id) -> list:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, obj_id):
        raise NotImplementedError
    
    @abstractmethod
    async def return_id_client(self, data):
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, obj_id):
        raise NotImplementedError
