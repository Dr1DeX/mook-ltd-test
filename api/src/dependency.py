from fastapi import (
    Depends,
    HTTPException,
    Security,
    security,
    status,
)

from sqlalchemy.ext.asyncio import AsyncSession

from redis import asyncio as redis

from src.dispatcher.users.auth.service import AuthService
from src.dispatcher.users.repository import UserRepository
from src.dispatcher.users.service import UserService
from src.exceptions import (
    TokenExpireExtension,
    TokenNotCorrectException,
)
from src.infrastructure.cache import get_redis_connection
from src.infrastructure.database import get_db_session


reusable_oauth2 = security.HTTPBearer()


async def get_user_repository(
    db_session: AsyncSession = Depends(get_db_session),
) -> UserRepository:
    return UserRepository(db_session=db_session)


async def get_auth_service(
    redis_client: redis.Redis = Depends(get_redis_connection),
    user_repository: UserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repository=user_repository, redis_client=redis_client)


async def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    auth_service: AuthService = Depends(get_auth_service),
    redis_client: redis.Redis = Depends(get_redis_connection),
) -> UserService:
    return UserService(
        user_repository=user_repository,
        auth_service=auth_service,
        redis_client=redis_client,
    )


async def get_request_user_id(
    auth_service: AuthService = Depends(get_auth_service),
    token: security.http.HTTPAuthorizationCredentials = Security(reusable_oauth2),
) -> int:
    try:
        user_id = await auth_service.get_user_id_from_access_token(
            token=token.credentials,
        )
    except TokenExpireExtension as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
    except TokenNotCorrectException as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)

    return user_id
