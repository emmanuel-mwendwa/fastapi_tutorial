from fastapi import FastAPI, status, HTTPException, Response, Depends
from pydantic import BaseModel

from fastapi.params import Body
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session

from . import models
from .database import engine, get_db

import psycopg2
import time

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

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

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
        
    return {"data": posts}

@app.post("/posts")
def create_posts(post: Post, db: Session = Depends(get_db)):
    
    # add new post
    new_post = models.Post(title=post.title, content=post.content, published=post.published)

    db.add(new_post)
    
    db.commit()

    # retrieve the new post created
    db.refresh(new_post)
    
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int):
    
    cursor.execute(""" SELECT * from posts WHERE id = %s""", (str(id)))

    post = cursor.fetchone()

    if not post:
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute(""" DELETE FROM posts WHERE id = %s returning * """, (str(id)))
    
    deleted_post = cursor.fetchone()

    conn.commit()

    if delete_post == None:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):

    cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %sRETURNING * """, (post.title, post.content, post.published, str(id)))

    updated_post = cursor.fetchone()

    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    

    return {"data": updated_post}