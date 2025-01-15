from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.dao.database import async_session_maker


class DatabaseSession:
    @staticmethod
    async def get_session(commit: bool = False) -> AsyncGenerator[AsyncSession, None]:
        async with async_session_maker() as session:
            try:
                yield session
                if commit:
                    await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    @staticmethod
    async def get_db() -> AsyncGenerator[AsyncSession, None]:
        """Dependency для получения сессии без автоматического коммита"""
        async for session in DatabaseSession.get_session(commit=False):
            yield session

    @staticmethod
    async def get_db_with_commit() -> AsyncGenerator[AsyncSession, None]:
        """Dependency для получения сессии с автоматическим коммитом"""
        async for session in DatabaseSession.get_session(commit=True):
            yield session


# Создаем экземпляр для удобного импорта
db = DatabaseSession()

# Примеры использования в роутах:
"""
@router.get("/items")
async def get_items(session: AsyncSession = Depends(db.get_db)):
    # Используем сессию без автоматического коммита
    ...

@router.post("/items")
async def create_item(session: AsyncSession = Depends(db.get_db_with_commit)):
    # Используем сессию с автоматическим коммитом
    ...
"""