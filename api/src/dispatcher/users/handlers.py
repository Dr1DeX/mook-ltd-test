from typing import Annotated

from fastapi import APIRouter, Depends

from src.dependency import get_user_service
from src.dispatcher.users.auth.schema import UserLoginSchema
from src.dispatcher.users.schema import UserCreateSchema
from src.dispatcher.users.service import UserService

router = APIRouter(prefix='/api/v1/user', tags=['user'])


@router.post('', response_model=UserLoginSchema)
async def create_user(
    body: UserCreateSchema,
    user_service: Annotated[UserService, Depends(get_user_service)],
):

    return await user_service.create_user(body=body)
