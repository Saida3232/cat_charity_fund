from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'cat charify dund'
    description: str = 'мяууу'
    database_url: str = 'sqlite+aiosqlite:///./fastapi_test.db'
    secret: str = 'SECRET'

    class Config():
        env_file = '.env'


settings = Settings()
