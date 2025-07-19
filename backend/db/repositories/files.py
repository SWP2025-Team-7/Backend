from typing import Optional
from backend.db.repositories.base import BaseRepository
from backend.models.files import FilesCreate, FilesInDB
import logging  

CREATE_FILE_QUERY = """
    INSERT INTO files (file_id, file_name, file_path, file_type, user_id, created_at)
    VALUES (:file_id, :file_name, :file_path, :file_type, :user_id, :created_at)
    RETURNING file_id, file_name, file_path, file_type, user_id, created_at;
"""

GET_FILE_BY_USER_ID_QUERY = """
    SELECT * FROM files WHERE user_id = :user_id;
"""

DELETE_FILE_BY_USER_ID_QUERY = """
    DELETE FROM files WHERE user_id = :user_id RETURNING user_id;
"""

class FilesRepository(BaseRepository):
    async def create_file(self, *, new_file: FilesCreate) -> FilesInDB:
        logging.info(f"Creating file: {new_file.file_name}")
        query_values = new_file.model_dump()
        file = await self.db.fetch_one(query=CREATE_FILE_QUERY, values=query_values)
        return FilesInDB(**file)
    
    async def get_files_by_user_id(self, *, user_id: int) -> Optional[FilesInDB]:
        file = await self.db.fetch_one(query=GET_FILE_BY_USER_ID_QUERY, values={"user_id": user_id})
        if file:
            return FilesInDB(**file)
        return None
    
    async def delete_file(self, *, user_id: int) -> bool:
        logging.info(f"Deleting file: {user_id}")
        await self.db.execute(query=DELETE_FILE_BY_USER_ID_QUERY, values={"user_id": user_id})