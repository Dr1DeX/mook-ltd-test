from dataclasses import dataclass

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.dispatcher.users.schema import UserCreateSchema
from src.dispatcher.users.models import UserProfile
from src.utils import hash_password


@dataclass
class UserRepository:
    db_session: AsyncSession

    async def create_user(self, data: UserCreateSchema) -> int:
        password = hash_password(password=data.password)
        user_data = data.dict(exclude_none=True)
        user_data['password'] = password

        query = insert(UserProfile).values(**user_data).returning(UserProfile.id)

        async with self.db_session as session:
            user_id: int = (await session.execute(query)).scalar()
            await session.commit()
            return user_id

    async def get_user_by_email(self, email: str) -> UserProfile | None:
        query = select(UserProfile).where(UserProfile.email == email)

        async with self.db_session as session:
            user = (await session.execute(query)).scalar_one_or_none()
            return user
