from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: srt
    sectre_key: srt
    debug: bool

    class Config:
        env_file = ".env"

settings = Settings()