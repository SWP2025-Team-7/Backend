import os
import base64
from fastapi import FastAPI, status, HTTPException, Request,Body,Depends
from pydantic import BaseModel
from backend.db.server import app
from starlette.status import HTTP_201_CREATED

from backend.models.bot_users import BotUsersCreate, BotUsersPublic
from backend.db.repositories.bot_users import BotUsersRepository
from backend.api.dependencies.database import get_repository
from backend.db.server import app


import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

class UserRegistration(BaseModel):
    userId: int
    alias: str
    
class DocumentUploading(BaseModel):
    userId: int
    file_in_bytes: str

@app.post("/register")
async def create_new_bot_user(
    new_bot_user: BotUsersCreate = Body(..., embed=True),
    bot_users_repo: BotUsersRepository = Depends(get_repository(BotUsersRepository)),
) -> BotUsersPublic:
    created_bot_user = await bot_users_repo.create_bot_user(new_bot_user=new_bot_user)

    return created_bot_user
"""
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
    
"""
