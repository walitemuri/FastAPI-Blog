from fastapi import FastAPI, HTTPException, Response, status, Depends
import psycopg2
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
import time
from . routers import post, user
from . import utils
from . import models
from .database import engine, SessionLocal, get_db
from sqlalchemy.orm import Session
from . import schemas


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


"""
Class: blogPost - Pydantic Schema for Blog Posts

Fields:
    title: (String) 
    content: (String)
"""


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

app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}

# GET Route: Gets the Posts
