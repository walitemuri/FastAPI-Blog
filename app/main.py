from fastapi import FastAPI
from .routers import post, user, auth
from . import models
from .database import engine
from . config import Settings
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# Root Route


@app.get("/")
def read_root():
    return {}
