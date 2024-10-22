from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
)

from src.dependency import get_auth_service
from src.dispatcher.users.auth.schema import (
    LogoutSchema,
    UserAuthSchema,
    UserLoginSchema,
)
from src.dispatcher.users.auth.service import AuthService


router = APIRouter(prefix='/api/v1/auth', tags=['auth'])


@router.post('/login', response_model=UserLoginSchema)
async def login(
    body: UserAuthSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return await auth_service.login(email=body.email, password=body.password)


@router.post(
    '/logout',
)
async def logout(
    body: LogoutSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    await auth_service.logout(token=body.token)
    return {'message': 'Successfully logged out'}
