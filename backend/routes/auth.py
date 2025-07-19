from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from backend.models.authorization import LoginResponse, Login

router = APIRouter(prefix="/login")

@router.post("/", name="authorization:login", response_model=LoginResponse,
    responses={
        status.HTTP_200_OK: {"description": "User logged in"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Login failed"}
    })
async def login():
    
    pass