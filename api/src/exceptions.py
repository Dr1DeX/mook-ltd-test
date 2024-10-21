class UserNotFoundException(Exception):
    detail = 'User not found'


class UserWrongPasswordException(Exception):
    detail = 'Wrong password'


class TokenNotCorrectException(Exception):
    detail = 'Not correct token'


class TokenExpireExtension(Exception):
    detail = 'Token expire'


class UserEmailUniqueException(Exception):
    detail = 'This email is already registered'
