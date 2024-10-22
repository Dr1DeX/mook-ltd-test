from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_PASSWORD: str = '123lol'
    DB_USER: str = 'ltd_user'
    DB_NAME: str = 'ltd'
    DB_DRIVER: str = 'postgresql+asyncpg'
    JWT_SECRET_KEY: str = 'mega-super-secret'
    JWT_ENCODE_ALGORYTHM: str = 'HS256'
    CACHE_HOST: str = 'localhost'
    CACHE_PORT: int = 6379
    CACHE_DB: int = 0
    CACHE_TTL: int = 100

    @property
    def db_url(self):
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


settings = Settings()
