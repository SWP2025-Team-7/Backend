from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi import UploadFile, File
from utils.parse_excel import parse_users_excel
from backend.models.users import UsersCreate, UsersUpdate
import shutil
import os

from backend.models.users import UsersCreate, UsersUpdate, UsersInDB, UsersPublic, UsersDocumentUpload, UsersDocumentUploadResponse
from backend.db.repositories.users import UsersRepository
from backend.api.dependencies.database import get_repository

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


@router.get("/{user_id}", response_model=UsersPublic, name="users:get-user",
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
    logging.info(user.start_date)
    logging.info(type(user.start_date))
    logging.info(user.start_date.isoformat())
    logging.info(type(user.start_date.isoformat()))
    logging.info(user.model_dump())
    return JSONResponse(status_code=status.HTTP_200_OK, content=user.model_dump())


@router.patch("/{user_id}", response_model=UsersPublic, name="users:update-user",
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


@router.delete("/{user_id}", name="users:delete-user",
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
@router.post("/upload_excel", name="users:upload-users-from-excel")
async def upload_users_from_excel(
    file: UploadFile = File(...),
    users_repo: UsersRepository = Depends(get_repository(UsersRepository)),
):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    inserted = 0
    updated = 0

    try:
        rows = parse_users_excel(temp_path)

        for row in rows:
            alias = row["alias"]
            existing_user = await users_repo.get_user_by_alias(alias=alias)

            if existing_user:
                user_update = UsersUpdate(**row)
                await users_repo.update_user(user_id=existing_user.user_id, user_update=user_update)
                updated += 1
            else:
                user_create = UsersCreate(**row)
                await users_repo.create_user(new_user=user_create)
                inserted += 1

        return {
            "status": "success",
            "inserted": inserted,
            "updated": updated
        }

    except Exception as e:
        return {"status": "error", "details": str(e)}

    finally:
        os.remove(temp_path)

