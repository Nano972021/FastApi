from multiprocessing import synchronize
from numbers import Integral
from fastapi import FastAPI
from fastapi import status, Response, HTTPException, Depends
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from .schemas import *
from typing import List
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        connection = psycopg2.connect(
            host="localhost", 
            database="fastapi", 
            user="postgres", 
            password="postgres2711",
            cursor_factory=RealDictCursor)
        cursor = connection.cursor()
        print("Database Connected Successfully")
        break
    except Exception as exception:
        print("Database Connection Failed")
        print("Exception")
        time.sleep(2)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message":"Hello World"}

