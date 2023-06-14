from pydantic import BaseSettings


class Settings(BaseSettings):
    database: str
    username: str
    password: str
    host: str
    port: str

    class Config:
        env_file = ".env"


settings = Settings()
