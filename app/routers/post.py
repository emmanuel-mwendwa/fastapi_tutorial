from fastapi import status, HTTPException, Response, Depends, APIRouter

from typing import List, Optional

from sqlalchemy.orm import Session

from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    tags=['Posts'],
    prefix="/posts"
)

@router.get("/", response_model=List[schemas.Post])
# query parameters to enable user to skip and limit posts recieved
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    
    # return posts created by user only 
    # .contains allows flexibility of providing keywords and seeing if it is in the search
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
        
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    # add new post using schema to ensure data validation
    # **post.dict() is for unpacking the schema
    # add user id to show who created the post
    new_post = models.Post(user_id=current_user.id, **post.dict())

    db.add(new_post)
    
    db.commit()

    # retrieve the new post created
    db.refresh(new_post)
    
    return new_post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()  

    if not post:
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    
    
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)  

    post = post_query.first()

    if post == None:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    if post.user_id != current_user.id:

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)

    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()