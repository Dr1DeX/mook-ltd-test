import logging

import bcrypt

from src.dispatcher.models import UserProfile
from src.exceptions import (
    UserNotFoundException,
    UserWrongPasswordException,
)


def validate_auth_user(user: UserProfile, password: str):
    if not user:
        logging.warning('This user not found')
        raise UserNotFoundException
    if not verify_password(plain_password=password, hashed_password=user.password):
        raise UserWrongPasswordException


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(
        password=plain_password.encode('utf-8'),
        hashed_password=hashed_password.encode('utf-8'),
    )
