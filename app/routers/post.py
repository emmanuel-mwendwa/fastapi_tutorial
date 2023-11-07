from fastapi import status, HTTPException, Response, Depends, APIRouter

from typing import List

from sqlalchemy.orm import Session

from .. import models, schemas

from ..database import get_db

router = APIRouter(
    tags=['Posts'],
    prefix="/posts"
)

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
        
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db)):
    
    # add new post using schema to ensure data validation
    # **post.dict() is for unpacking the schema
    new_post = models.Post(**post.dict())

    db.add(new_post)
    
    db.commit()

    # retrieve the new post created
    db.refresh(new_post)
    
    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()  

    if not post:
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)  

    if post.first() == None:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    post.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.CreatePost, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = post_query.first()

    if updated_post == None:
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    post_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()