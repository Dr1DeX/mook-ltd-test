from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from src.settings import settings

engine = create_async_engine(
    url=settings.db_url,
    future=True,
    echo=True,
    pool_pre_ping=True,
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    autocommit=False,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncSession:
    async with AsyncSessionFactory() as session:
        yield session
