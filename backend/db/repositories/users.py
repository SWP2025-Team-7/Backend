from typing import Optional
from backend.db.repositories.base import BaseRepository
from backend.models.users import UsersCreate, UsersUpdate, UsersInDB
 
 
# CREATE_USERS_QUERY = """
#     INSERT INTO users (user_id, alias, mail, name, surname, patronymic, phone_number, citizens, duty_to_work, duty_status, grant_amount, duty_period, company, resume_path, position, start_date, end_date, salary, working_reference_path, ndfl1_path, ndfl2_path, ndfl3_path, ndfl4_path)
#     VALUES (:user_id, :alias, :mail, :name, :surname, :patronymic, :phone_number, :citizens, :duty_to_work, :duty_status, :grant_amount, :duty_period, :company, :resume_path, :position, :start_date, :end_date, :salary, :working_reference_path, :ndfl1_path, :ndfl2_path, :ndfl3_path, :ndfl4_path)
#     RETURNING id, user_id, alias, mail, name, surname, patronymic, phone_number, citizens, duty_to_work, duty_status, grant_amount, duty_period, company, resume_path, position, start_date, end_date, salary, working_reference_path, ndfl1_path, ndfl2_path, ndfl3_path, ndfl4_path;
# """

CREATE_USERS_QUERY = """
    INSERT INTO users (user_id, alias, mail, name, surname, patronymic)
    VALUES (:user_id, :alias, :mail, :name, :surname, :patronymic)
    RETURNING id, user_id, alias, mail, name, surname, patronymic, phone_number, citizens, duty_to_work, duty_status, grant_amount, duty_period, company, resume_path, position, start_date, end_date, salary, working_reference_path, ndfl1_path, ndfl2_path, ndfl3_path, ndfl4_path;
"""

GET_USER_BY_USER_ID_QUERY = """
    SELECT * FROM users WHERE user_id = :user_id;
"""

DELETE_USER_BY_USER_ID_QUERY = """
    DELETE FROM users WHERE user_id = :user_id RETURNING id;
"""
class UsersRepository(BaseRepository):
 
    async def create_users(self, *, new_user: UsersCreate) -> UsersInDB:
        query_values = new_user.dict()
        user = await self.db.fetch_one(query=CREATE_USERS_QUERY, values=query_values)
 
        return UsersInDB(**user)
    
    async def get_user_by_id(self, user_id: int) -> Optional[UsersInDB]:
        user_record = await self.db.fetch_one(query=GET_USER_BY_USER_ID_QUERY, values={"user_id": user_id})
        if user_record:
            return UsersInDB(**user_record)
        return None
    
    async def update_user(self, *, user_id: int, user_update: UsersUpdate) -> Optional[UsersInDB]:
        update_data = user_update.dict(exclude_unset=True)  # берём только поля, которые обновляем
        if not update_data:
            return None  # нечего обновлять

        set_clause = ", ".join([f"{field} = :{field}" for field in update_data.keys()])
        query = f"""
            UPDATE users SET {set_clause} WHERE user_id = :user_id RETURNING *;
        """
        update_data["user_id"] = user_id
        updated_record = await self.db.fetch_one(query=query, values=update_data)
        if updated_record:
            return UsersInDB(**updated_record)
        return None

    async def delete_user(self, *, user_id: int) -> bool:
        deleted = await self.db.execute(query=DELETE_USER_BY_USER_ID_QUERY, values={"user_id": user_id})
        return deleted > 0