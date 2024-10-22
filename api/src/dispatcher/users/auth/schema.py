from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    user_id: int
    access_token: str


class UserAuthSchema(BaseModel):
    email: str
    password: str


class LogoutSchema(BaseModel):
    token: str
