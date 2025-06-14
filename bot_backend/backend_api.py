import os
from fastapi import FastAPI, status, HTTPException
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI()

@app.get("/")
def home_page():
    return {"message": "Home Page"}

@app.post("/users/register", status_code=status.HTTP_200_OK)
def register_user():
    logging.warning("User registration is not completed")
    return 


@app.post("/documents/upload", status_code=status.HTTP_200_OK)
async def upload_document():
    logging.warning("Uploading documents is not completed")

@app.get("/documents/extract", status_code=status.HTTP_200_OK)
async def extract_document():
    logging.warning("Extraction documents is not completed")
