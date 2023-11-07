from fastapi import FastAPI, status, HTTPException, Response, Depends
from typing import List

from fastapi.params import Body
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from . import models, schemas, utils
from .database import engine, get_db

import psycopg2
import time


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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

@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
        
    return posts

@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db)):
    
    # add new post using schema to ensure data validation
    # **post.dict() is for unpacking the schema
    new_post = models.Post(**post.dict())

    db.add(new_post)
    
    db.commit()

    # retrieve the new post created
    db.refresh(new_post)
    
    return new_post


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()  

    if not post:
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    return post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)  

    if post.first() == None:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    post.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = post_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    post_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    # store the hashed_password in the pydantic model 
    user.password = hashed_password

    new_user = models.User(**user.dict())

    db.add(new_user)

    db.commit()

    db.refresh(new_user)

    return new_user