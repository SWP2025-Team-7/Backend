from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from fastapi.responses import JSONResponse

from backend.models.users import UsersCreate, UsersUpdate, UsersInDB, UsersPublic
from backend.db.repositories.users import UsersRepository

from backend.models.files import FilesCreate, FilesInDB, FilesPublic, FilesExtract, FilesExtractOutput, FilesExtractResponse, File_Type
from backend.db.repositories.files import FilesRepository

from backend.api.dependencies.database import get_repository

from datetime import datetime, date
import requests as re

import os

import json

import logging

router = APIRouter(prefix="/users")

@router.post("/", response_model=UsersPublic, name="users:create-user", 
             responses={
                 status.HTTP_400_BAD_REQUEST: {"model": UsersPublic, "description": "User already exists", },
                 status.HTTP_201_CREATED: {"model": UsersPublic, "description": "User created"},
                 status.HTTP_200_OK: {"model": UsersPublic, "description": "User updated"}
                 })
async def create_user(
    new_user: UsersCreate,
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UsersCreate:
    user = await users_repo.get_user_by_id(user_id=new_user.user_id)
    if user:
        if user.alias == new_user.alias:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=user.model_dump())
        else:
            user = await users_repo.update_user(user_id=new_user.user_id, user_update=UsersUpdate(alias=new_user.alias))
            return JSONResponse(status_code=status.HTTP_200_OK, content=user.model_dump())
    created_user = await users_repo.create_user(new_user=new_user)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_user.model_dump())

@router.get("/", response_model=list[UsersPublic], name="users:get-users")
async def get_users(
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
):
    return JSONResponse(status_code=status.HTTP_200_OK, content=[user.model_dump() for user in await users_repo.get_all_users()])

user_router = APIRouter(prefix="/{user_id}")

@user_router.get("/", response_model=UsersPublic, name="users:get-user",
            responses={
                status.HTTP_404_NOT_FOUND: {"description": "User not found"},
                status.HTTP_200_OK: {"model": UsersPublic, "description": "User found"}
                })
async def get_user_by_id( 
    user_id: int,
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
):
    user = await users_repo.get_user_by_id(user_id=user_id)
    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"})
    return JSONResponse(status_code=status.HTTP_200_OK, content=user.model_dump())

@user_router.patch("/", response_model=UsersPublic, name="users:update-user",
              responses={
                  status.HTTP_404_NOT_FOUND: {"description": "User not found"},
                  status.HTTP_200_OK: {"model": UsersPublic, "description": "User updated"}
                  })
async def update_user(
    user_id: int,
    user_update: UsersUpdate,
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
):
    user = await users_repo.get_user_by_id(user_id=user_id)
    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"})
    
    updated_user = await users_repo.update_user(user_id=user_id, user_update=user_update)
    return JSONResponse(status_code=status.HTTP_200_OK, content=updated_user.model_dump())

@user_router.delete("/", name="users:delete-user",
               responses={
                   status.HTTP_404_NOT_FOUND: {"description": "User not found"},
                   status.HTTP_200_OK: {"description": "User deleted"}
               })
async def delete_user(
    user_id: int,
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
):
    user = await users_repo.get_user_by_id(user_id=user_id)
    if not user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"})
    await users_repo.delete_user(user_id=user_id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"detail": "User deleted"})

files_router = APIRouter(prefix="/documents")

@files_router.post("/extract", response_model=FilesExtractResponse, name="documents:extract-file",
                   status_code=status.HTTP_200_OK)
async def upload_document(
    user_id: int,
    user_document_upload: FilesExtract,
    users_repo: UsersRepository = Depends(get_repository(UsersRepository))
):
    # existing_user = await users_repo.get_user_by_id(user_document_upload.user_id)
    # if not existing_user:
    #     raise HTTPException(status_code=404, detail="User not found")
    
    # 
    data = {
        "file_path": user_document_upload.file_path
    }
    ans = re.post(url=f"{os.getenv('N8N_URL')}", data=json.dumps(data), headers={'Content-Type': 'application/json'})
    logging.info(f"{ans}")
    return ans.json()

@files_router.post("/", response_model=UsersPublic, name="documents:upload-file",
            responses={
                status.HTTP_404_NOT_FOUND: {"description": "User not found"},
                status.HTTP_200_OK: {"model": UsersPublic, "description": "File uploaded"}
                })
async def upload_document(
    user_id: int,
    uploaded_file: UploadFile,
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    files_repo: FilesRepository = Depends(get_repository(FilesRepository))
):
    existing_user = await users_repo.get_user_by_id(user_id=user_id)
    if not existing_user:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": "User not found"})
    
    
    
    file = FilesCreate(
        file_name=uploaded_file.filename,
        file_path="path",
        file_type=File_Type.working_reference.value,
        user_id=user_id,
        created_at=datetime.now().date()
    )
    created_file = await files_repo.create_file(new_file=file)
    return JSONResponse(status_code=status.HTTP_200_OK, content=created_file.model_dump())



user_router.include_router(files_router)
router.include_router(user_router)