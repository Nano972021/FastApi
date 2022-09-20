from fastapi import status, Response, HTTPException, Depends, APIRouter

from app.oauth2 import get_current_user
from .. import models
from ..database import get_db
from ..schemas import *
from typing import List
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(
    prefix="/posts",
    tags = ['Posts']
)
# Get all posts------------------------------------
@router.get("/", response_model=List[Post])
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    # cursor.execute("""
    # SELECT * FROM posts
    # """)
    # posts = cursor.fetchall()
    # print(posts)

    posts = db.query(models.Post).all()
    return posts


# Create a post------------------------------------
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    # cursor.execute("""
    # INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *
    # """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # connection.commit()

    new_post = models.Post(**post.dict())
    db.add(new_post) # add it to db
    db.commit() # commit changes
    db.refresh(new_post) # retrieve newly added data
    return new_post # return the new post


# Get the latest post-------------------------------
@router.get("/latest")
def get_latest():
    # cursor.execute("""
    # SELECT * FROM posts WHERE created_at = (SELECT MAX(created_at) FROM posts)
    # """)
    # l = cursor.fetchone()
    # return l
    pass


# Get an indivisual post----------------------------
@router.get("/{id}", response_model=Post)
def get_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    # cursor.execute("""
    # SELECT * FROM posts WHERE id = %s
    # """, (str(id)))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post: # Post not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} does not exist")
    return post


# Delete a specific post-----------------------------
@router.delete("/{id}", response_model=Post)
def delete_post(id: int, status_code=status.HTTP_204_NO_CONTENT, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    # cursor.execute("""
    # DELETE FROM posts WHERE id = %s RETURNING *
    # """, (str(id)))
    # post = cursor.fetchone()
    # connection.commit()
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} does not exist")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# Update a specific post ----------------------------
@router.put("/{id}", response_model=Post)
def update_post(id: str, update: PostCreate, db: Session = Depends(get_db), user_id: int = Depends(get_current_user)):
    # cursor.execute("""
    # UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *
    # """, (post.title, post.content, post.published, str(id)))
    # post = cursor.fetchone()
    # connection.commit()
    
    query = db.query(models.Post).filter(models.Post.id == id)
    post = query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"post with id: {id} does not exist")
    query.update(update.dict(), synchronize_session=False)
    db.commit()

    return query.first()
