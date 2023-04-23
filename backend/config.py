from os import getenv

from dotenv import load_dotenv
load_dotenv()

POSTGRES_USER = getenv('POSTGRES_USER')
POSTGRES_PASSWORD = getenv('POSTGRES_PASSWORD')
POSTGRES_DB = getenv('POSTGRES_DB')
HOST = getenv('HOST')

SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = "HS256"

