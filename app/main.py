from fastapi import FastAPI, HTTPException, Response, status, Depends
import psycopg2
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
import time
from . import models
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


"""
Class: blogPost - Pydantic Schema for Blog Posts

Fields:
    title: (String) 
    content: (String)
"""


class blogPost(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi-blog',
                                user='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was sucessful")
        break
    except Exception as e:
        print("Connection to db Failed")
        print(e)
        time.sleep(2)
# Home Route


@app.get("/")
def read_root():
    return {"Hello": "World"}

# GET Route: Gets the Posts


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    # cursor.execute(""" SELECT * FROM "blogPosts" ORDER BY post_id""")
    # posts = cursor.fetchall()
    # print(posts)
    return {"data": posts}

# Create Post Route


@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_posts(post: blogPost, db: Session = Depends(get_db)):

    newPost = models.Post(**post.dict())
    db.add(newPost)
    db.commit()
    db.refresh(newPost)
    # cursor.execute("""INSERT INTO "blogPosts" (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # newPost = cursor.fetchone()
    # conn.commit()
    return {"data": newPost}


# Retrieve One Post


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.post_id == id).first()

    # cursor.execute(
    #     """SELECT * FROM "blogPosts" WHERE post_id = %s""", (str(id), ))
    # post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} does not exist")
    return {"post_detail": post}

# Delete Post


@app.delete("/posts/{id}")
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


@app.put("/posts/{id}")
def update_post(id: int, updated_post: blogPost,  db: Session = Depends(get_db)):

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
    return {"post_detail": post_query.first()}
