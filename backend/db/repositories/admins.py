from typing import Optional
from backend.db.repositories.base import BaseRepository
from backend.models.admins import AdminsCreate, AdminsInDB
import logging  

CREATE_ADMIN_QUERY = """
    INSERT INTO admins (username, hashed_password)
    VALUES (:username, :hashed_password)
    RETURNING id, username, hashed_password;
"""

GET_ADMIN_BY_USERNAME_QUERY = """
    SELECT * FROM admins WHERE username = :username;
"""

DELETE_ADMIN_BY_USERNAME_QUERY = """
    DELETE FROM admins WHERE username = :username RETURNING username;
"""

class AdminsRepository(BaseRepository):
    async def get_admin_by_username(self, *, username: str) -> Optional[AdminsInDB]:
        logging.info(f"Getting admin: {username}")
        admin = await self.db.fetch_one(query=GET_ADMIN_BY_USERNAME_QUERY, values={"username": username})
        if admin:
            return AdminsInDB(**admin)
        return None
    
    async def create_admin(self, *, new_admin: AdminsCreate) -> AdminsInDB:
        logging.info(f"Creating admin: {new_admin.username}")
        query_values = new_admin.model_dump()
        admin = await self.db.fetch_one(query=CREATE_ADMIN_QUERY, values=query_values)
        return AdminsInDB(**admin)
    
    async def delete_admin(self, *, username: str) -> bool:
        logging.info(f"Deleting admin: {username}")
        await self.db.execute(query=DELETE_ADMIN_BY_USERNAME_QUERY, values={"username": username})