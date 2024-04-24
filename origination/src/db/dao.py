from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(ABC):
    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def create(self, obj):
        raise NotImplementedError

    @abstractmethod
    async def update_status(self, obj, status: str):
        raise NotImplementedError
