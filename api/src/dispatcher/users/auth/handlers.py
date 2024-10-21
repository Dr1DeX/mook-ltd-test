from typing import Annotated

from fastapi import APIRouter, Depends

from src.dependency import get_auth_service
from src.dispatcher.users.auth.schema import UserLoginSchema
from src.dispatcher.users.auth.service import AuthService
from src.dispatcher.users.schema import UserCreateSchema

router = APIRouter(prefix='/api/v1/auth', tags=['auth'])


@router.post('/login', response_model=UserLoginSchema)
async def login(
    body: UserCreateSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return await auth_service.login(email=body.email, password=body.password)
