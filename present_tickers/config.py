"""Flask configuration variables."""
from os import getenv
from dotenv import load_dotenv


load_dotenv()


class Config:
    """Set Flask configuration from .env file."""

    # General Config
    FLASK_APP = getenv('FLASK_APP')
    FLASK_ENV = getenv('FLASK_ENV')

    # Database
    SQLALCHEMY_DATABASE_URI = getenv("SQLALCHEMY_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False