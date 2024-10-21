import logging
from dataclasses import dataclass

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.dispatcher.users.auth.service import AuthService
from src.dispatcher.users.repository import UserRepository
from src.dispatcher.users.schema import UserCreateSchema
from src.dispatcher.users.auth.schema import UserLoginSchema


@dataclass
class UserService:
    user_repository: UserRepository
    auth_service: AuthService

    async def create_user(self, body: UserCreateSchema) -> UserLoginSchema:
        try:
            user_id = await self.user_repository.create_user(data=body)
            access_token = self.auth_service.generate_access_token(user_id=user_id)
            return UserLoginSchema(user_id=user_id, access_token=access_token)
        except IntegrityError:
            logging.error(f'This email is exists: {body.email}')
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Email unique'
            )
