import os

from dotenv import load_dotenv


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


class BaseConfig:
    """Base configuration."""

    ADMIN_LOGIN = os.environ.get("ADMIN_LOGIN")
    ADMIN_PASSWD = os.environ.get("ADMIN_PASSWD")

    # POSTGRES_DB = os.environ.get("POSTGRES_DB")
    # POSTGRES_USER = os.environ.get("POSTGRES_USER")
    # POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    # POSTGRES_HOST = os.environ.get("POSTGRES_HOST")

    DB_URL = "postgresql://frghjk:asdfgyu76trfvbj@db:5432/fewfewfwef"

class DevelopmentConfig:
    """Development configuration."""


config = dict(base=BaseConfig, development=DevelopmentConfig)
