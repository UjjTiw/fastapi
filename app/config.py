import os
from dotenv import load_dotenv
from urllib.parse import quote

# Explicitly specify the path to the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
load_dotenv(dotenv_path)

# Fetching the environment variables
DATABASE_PASSWORD = quote(os.getenv('DATABASE_PASSWORD'))
DATABASE_HOSTNAME = os.getenv('DATABASE_HOSTNAME')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_NAME = os.getenv('DATABASE_NAME')


SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
