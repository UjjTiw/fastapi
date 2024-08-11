from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2 
from psycopg2.extras import RealDictCursor
import time
from .config import DATABASE_HOSTNAME, DATABASE_NAME, DATABASE_PASSWORD, DATABASE_PORT,DATABASE_USERNAME

# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:@Ujjwal9798@localhost/fastapi' wrong
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:%40Ujjwal9798@localhost/fastapi' correct

from urllib.parse import quote

SQLALCHEMY_DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOSTNAME}:{DATABASE_PORT}/{DATABASE_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db(): # Creates the sessioon for the databaeseß
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()










while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='@Ujjwal9798', cursor_factory=RealDictCursor)

        cursor = conn.cursor() # doesnt gives the column nmes

        print("Database connection ws successful!!!")
        break

    except Exception as e:
        print("Connection to the database failed")
        print("Error: ", e)
        time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1},
            {"title": "favourite foods", "content": "I like Pizza", "id": 2}]


