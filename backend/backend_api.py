import os
import base64
from fastapi import FastAPI, status, HTTPException, Request,Body,Depends
from pydantic import BaseModel
from backend.db.server import app
from starlette.status import HTTP_201_CREATED
from backend.routes.students import router as students_router
from backend.routes.user import router as user_router

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

@app.get("/")
def home_page():
    return {"message": "Home Page"}
    
app.include_router(router=students_router)
app.include_router(router=user_router)