from typing import Callable, Type
from databases import Database
 
from fastapi import Depends
from starlette.requests import Request
 
from backend.db.repositories.base import BaseRepository

import logging
 
 
def get_database(request: Request) -> Database:
    logging.info(f"Getting database: {request}")
    return request.app.state._db
 
 
def get_repository(Repo_type: Type[BaseRepository]) -> Callable:
    logging.info(f"Getting repository: {Repo_type}")
    def get_repo(db: Database = Depends(get_database)) -> Type[BaseRepository]:
        return Repo_type(db)
 
    return get_repo
 
 