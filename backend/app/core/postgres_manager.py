from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker


from sqlalchemy import NullPool, exc

from .pydantic_settings_config import settings

class DatabaseManager:
    def __init__(self):
        self.database_url = settings.database_url
        if not self.database_url:
            raise ValueError("Database URL not configured")
        
        str_url = str(self.database_url)
        pool_class = NullPool if "test" in str_url else None

        self.engine = create_async_engine(
            str_url,
            echo = settings.enviroment == "development",
            pool_size = settings.database_pool_size,
            max_overflow = settings.database_max_overflow,
            pool_pre_ping = True,
            poolclass = pool_class
        )

        self.async_session_factory = async_sessionmaker(
            self.engine,
            expire_on_commit = False,
            class_ = AsyncSession
        )

    @asynccontextmanager
    async def get_session(self):
        async with self.async_session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()


db_manage = DatabaseManager()

async def get_db():
    async with db_manage.get_session() as session:
        yield session



