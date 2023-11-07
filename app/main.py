from fastapi import FastAPI

from psycopg2.extras import RealDictCursor

from . import models
from .database import engine
from .routers import post, user, auth

import psycopg2
import time


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


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


@app.get("/")
async def root():

    return {"message": "Hello World"}
