from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from psycopg2.extras import RealDictCursor

import psycopg2
import time

# How to connect to a database
# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:root@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Run until we get a connection
while True:
    # set up connection to database
    try:

        # conn = psycopg2.connect(host, database, user, password)
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='root', cursor_factory=RealDictCursor)

        cursor = conn.cursor()

        print("Database connection was successfull!")

        break

    except Exception as error:

        print("Connecting to database failed!")

        print("Error: ", error)

        time.sleep(2)