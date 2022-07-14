from pydantic import BaseSettings


class Settings(BaseSettings):
    MONGO_DETAILS: str
    RABBIT_URL: str
    RABBIT_QUEUE_NAME: str

    class Config:
        env_file = ".env"


settings = Settings()
