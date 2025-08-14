from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    openai_api_key: str
    wikipedia_api_url: str
    database_url: str

    class Config:
        env_file = ".env"


settings = Settings()
