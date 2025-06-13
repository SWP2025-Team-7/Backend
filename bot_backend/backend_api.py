import os
from fastapi import FastAPI
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI()

@app.get("/")
def home_page():
    return {"message": "Home Page"}

@app.post("/users/register")
def register_user():
    logging.warning("User registration is not completed")

