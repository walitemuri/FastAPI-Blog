from .. import models, schemas
from fastapi import FastAPI, HTTPException, Response, status, Depends, APIRouter
from sqlalchemy.orm import Session
from .. database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# GET Route: Gets the Posts


@router.get("/", response_model=list[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # cursor.execute(""" SELECT * FROM "blogPosts" ORDER BY post_id""")
    # posts = cursor.fetchall()
    # print(posts)
    return posts

# Create Post Route


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.CreatePost, db: Session = Depends(get_db)):

    newPost = models.Post(**post.dict())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    # cursor.execute("""INSERT INTO "blogPosts" (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # newPost = cursor.fetchone()
    # conn.commit()
    return newPost


# Retrieve One Post


@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.post_id == id).first()

    # cursor.execute(
    #     """SELECT * FROM "blogPosts" WHERE post_id = %s""", (str(id), ))
    # post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    return post

# Delete Post


@router.delete("/{id}")
def delete_post(id: int,  db: Session = Depends(get_db)):

    deleted_post = db.query(models.Post).filter(models.Post.post_id == id)
    # cursor.execute(
    #     """DELETE FROM "blogPosts" WHERE post_id = %s RETURNING *""", (str(id), ))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# Update Post


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.UpdatePost,  db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.post_id == id)
    post = post_query.first()
    # cursor.execute("""UPDATE "blogPosts" SET title = %s, content = %s, published = %s WHERE post_id = %s RETURNING *""",
    #                (post.title, post.content, post.published, (str(id), )))
    # update_post = cursor.fetchone()
    # conn.commit()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
