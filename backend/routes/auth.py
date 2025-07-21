import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from passlib.context import CryptContext
from typing import Optional, Annotated

from datetime import datetime, timedelta
from jose import jwt

from backend.models.auth import Token, Login
from backend.models.admins import AdminsCreate
from backend.db.repositories.admins import AdminsRepository

from backend.api.dependencies.database import get_repository


router = APIRouter(prefix="/auth", tags=["Authorization"])

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post("/", name="authorization:create-user", 
    responses={
        status.HTTP_201_CREATED: {"description": "User created"},
        status.HTTP_400_BAD_REQUEST: {"description": "User already exists"}
    })
async def create_user(
    user: Login,
    admins_repo: AdminsRepository = Depends(get_repository(AdminsRepository))
):
    admin = await admins_repo.get_admin_by_username(username=user.username)
    if admin:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    hashed_password = bcrypt_context.hash(user.password)
    await admins_repo.create_admin(new_admin=AdminsCreate(username=user.username, hashed_password=hashed_password))
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"detail": "User created"})

@router.post("/token", name="authorization:login", response_model=Token,
    responses={
        status.HTTP_200_OK: {"description": "User logged in"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Login failed"}
    })
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    admins_repo: AdminsRepository = Depends(get_repository(AdminsRepository))
):
    login = Login(username=form_data.username, password=form_data.password)
    admin = await admins_repo.get_admin_by_username(username=login.username)
    if not admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    if not bcrypt_context.verify(login.password, admin.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
    token = create_access_token(data={"username": login.username}, timedelta=timedelta(minutes=20))
    
    return JSONResponse(status_code=status.HTTP_200_OK, content={"access_token": token, "token_type": "bearer"})

def create_access_token(data: dict, timedelta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm=os.getenv("ALGORITHM"))
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        username: str = payload.get("username")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        return username
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    
user_dependency = Annotated[dict, Depends(get_current_user)]