import os
import base64
from fastapi import FastAPI, status, HTTPException, Request
from pydantic import BaseModel
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

app = FastAPI()

class UserRegistration(BaseModel):
    userId: int
    alias: str
    
class DocumentUploading(BaseModel):
    userId: int
    file_in_bytes: str

@app.get("/")
def home_page():
    return {"message": "Home Page"}

@app.get("/users/register", status_code=status.HTTP_200_OK)
def register_user(r: UserRegistration):
    logging.info(f"Data for registrating: userId:{r.userId}, alias:{r.alias}")
    logging.warning("User registration is not completed")
    return {"message": ""}


@app.get("/documents/upload", status_code=status.HTTP_200_OK)
async def upload_document(r: DocumentUploading):
    logging.info(f"Upploading file from userId: {r.userId}")
    with open("file.pdf", "wb") as f:
        f.write(r.file_in_bytes.encode("latin-1"))
    logging.warning("Uploading documents is not completed")
    

