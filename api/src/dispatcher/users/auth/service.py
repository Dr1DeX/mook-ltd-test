import datetime
import logging
from dataclasses import dataclass
from datetime import datetime as dt, timedelta

from fastapi import HTTPException, status
from jose import jwt, JWTError

from src.dispatcher.users.auth.schema import UserLoginSchema
from src.dispatcher.users.repository import UserRepository
from src.exceptions import (
    TokenExpireExtension,
    TokenNotCorrectException,
    UserNotFoundException,
    UserWrongPasswordException,
)
from src.settings import settings
from src.utils import validate_auth_user


@dataclass
class AuthService:
    user_repository: UserRepository

    async def login(self, email: str, password: str) -> UserLoginSchema:
        try:
            user = await self.user_repository.get_user_by_email(email=email)
            validate_auth_user(user=user, password=password)

            logging.info('Validate user success!')

            access_token = self.generate_access_token(user_id=user.id)
            return UserLoginSchema(user_id=user.id, access_token=access_token)
        except UserNotFoundException as e:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.detail)
        except UserWrongPasswordException as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail
            )

    def generate_access_token(self, user_id: int) -> str:
        payload = {
            'user_id': user_id,
            'expire': (dt.now(tz=datetime.UTC) + timedelta(days=7)).timestamp(),
        }
        encoded_jwt = jwt.encode(
            claims=payload,
            key=settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ENCODE_ALGORYTHM,
        )
        logging.info('JWT_ENCODE success!')
        return encoded_jwt

    async def get_user_id_from_access_token(self, token: str) -> int:
        try:
            payload = jwt.decode(
                token=token,
                key=settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ENCODE_ALGORYTHM],
            )
        except JWTError as e:
            logging.error(f'This payload to expire: {e}')
            raise TokenExpireExtension
        if payload['expire'] < dt.now().timestamp():
            logging.error(f'This payload dont correct: {payload}')
            raise TokenNotCorrectException
        return payload['user_id']
