from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_PASSWORD: str = 'mega-pass'
    DB_USER: str = 'postgres'
    DB_NAME: str = 'ltd'
    DB_DRIVER: str = 'postgresql+asyncpg'

    @property
    def db_url(self):
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


settings = Settings()
