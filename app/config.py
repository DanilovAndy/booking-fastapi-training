import os
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=os.path.join(os.path.dirname(__file__), '../.env'),
                                      env_file_encoding='utf-8', extra='ignore')

    MODE: Literal["DEV", "TEST", "PROD"]
    LOG_LEVEL: Literal["INFO", "DEBUG", "TRACE", "WARN", "ERROR", "FATAL"]

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    ACCESS_TOKEN_EXPIRES_MINUTES: int
    REFRESH_TOKEN_EXPIRES_MINUTES: int

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    REDIS_HOST: str
    REDIS_PORT: int

    SENTRY_DSN: str
    SENTRY_TRACES_SAMPLE_RATE: float
    SENTRY_PROFILES_SAMPLE_RATE: float

    ENABLE_ADMIN: bool

    SECRET_KEY: str
    ALGORITHM: str


settings = Settings()
