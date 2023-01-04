from fastapi import FastAPI, Response, status
import psycopg2
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
import time
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
    likes: int


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
def get_posts():
    cursor.execute(""" SELECT * FROM "blogPosts" """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

# Create Post Route


@app.post("/createpost", status_code=status.HTTP_201_CREATED)
def create_posts(post: blogPost):
    cursor.execute("""INSERT INTO "blogPosts" (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    newPost = cursor.fetchone()
    conn.commit()
    return {"data": newPost}


# Retrieve One Post
@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute(
        """SELECT * FROM "blogPosts" WHERE post_id = %s""", (str(id)))
    post = cursor.fetchone()
    return {"data": post}

# @app.get("/post/{id}")
# def get_post():
#     return
