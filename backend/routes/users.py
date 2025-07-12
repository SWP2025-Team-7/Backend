from fastapi import APIRouter, Depends, HTTPException, status

from backend.models.users import UsersCreate, UsersUpdate, UsersInDB, UsersPublic, UsersDocumentUpload, UsersDocumentUploadResponse
from backend.db.repositories.users import UsersRepository
from backend.api.dependencies.database import get_repository

import requests as re
import json

import os

import logging

router = APIRouter(prefix="/users")

@router.post("/", response_model=UsersPublic, name="users:create-user", status_code=status.HTTP_201_CREATED)
async def create_user(
    new_user: UsersCreate,
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
) -> UsersCreate:
    created_user = await users_repo.create_users(new_user=new_user)
    return created_user


@router.get("/{user_id}", response_model=UsersPublic, name="users:get-user", status_code=status.HTTP_302_FOUND)
async def get_user_by_id(
    user_id: int,
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
):
    user = await users_repo.get_user_by_id(user_id=user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UsersPublic)
async def update_user(
    user_id: int,
    user_update: UsersUpdate,
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
):
    existing_user = await users_repo.get_user_by_id(user_id=user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    updated_user = await users_repo.update_user(user_id=user_id, user_update=user_update)
    return updated_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
):
    deleted = await users_repo.delete_user(user_id=user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@router.post("/{user_id}/documents/upload", response_model=UsersDocumentUploadResponse, status_code=status.HTTP_200_OK)
async def upload_document(
    user_id: int,
    user_document_upload: UsersDocumentUpload,
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

