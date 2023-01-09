from typing import Optional
from .. import oauth2
from .. import models, schemas
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# GET Route: Gets the Posts


@router.get("/", response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    """
    Filters:
        Contains (search): Finds posts containing entered characters
        Limit : Max # of posts to return
        Offset: Skip X number of entries
    """
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.post_id, isouter=True).group_by(models.Post.post_id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # cursor.execute(""" SELECT * FROM "blogPosts" ORDER BY post_id""")
    # posts = cursor.fetchall()
    # print(posts)
    return results

# Create Post Route


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    newPost = models.Post(owner_id=current_user.id, **post.dict())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    # cursor.execute("""INSERT INTO "blogPosts" (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # newPost = cursor.fetchone()
    # conn.commit()
    return newPost


# Retrieve One Post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)) -> schemas.PostOut:

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.post_id, isouter=True).group_by(models.Post.post_id).filter(models.Post.post_id == id).first()

    # cursor.execute(
    #     """SELECT * FROM "blogPosts" WHERE post_id = %s""", (str(id), ))
    # post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    return post

# Delete Post


@router.delete("/{id}")
def delete_post(id: int,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)) -> None:

    deleted_post_query = db.query(
        models.Post).filter(models.Post.post_id == id)
    deleted_post = deleted_post_query.first()
    # cursor.execute(
    #     """DELETE FROM "blogPosts" WHERE post_id = %s RETURNING *""", (str(id), ))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perfom action")

    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update Post


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.UpdatePost,  db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.post_id == id)
    post = post_query.first()
    # cursor.execute("""UPDATE "blogPosts" SET title = %s, content = %s, published = %s WHERE post_id = %s RETURNING *""",
    #                (post.title, post.content, post.published, (str(id), )))
    # update_post = cursor.fetchone()
    # conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform action")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
