from db.repositories.base import BaseRepository
from models.users import UsersCreate, UsersUpdate, UsersInDB
 
 
CREATE_USERS_QUERY = """
    INSERT INTO users (user_id, alias, mail, name, surname, patronymic, phone_number, citizens, duty_to_work, duty_status, grant_amount, duty_period, company, resume_path, position, start_date, end_date, salary, working_reference_path, ndfl1_path, ndfl2_path, ndfl3_path, ndfl4_path)
    VALUES (:user_id, :alias, :mail, :name, :surname, :patronymic, :phone_number, :citizens, :duty_to_work, :duty_status, :grant_amount, :duty_period, :company, :resume_path, :position, :start_date, :end_date, :salary, :working_reference_path, :ndfl1_path, :ndfl2_path, :ndfl3_path, :ndfl4_path)
    RETURNING id, user_id, alias, mail, name, surname, patronymic, phone_number, citizens, duty_to_work, duty_status, grant_amount, duty_period, company, resume_path, position, start_date, end_date, salary, working_reference_path, ndfl1_path, ndfl2_path, ndfl3_path, ndfl4_path;
"""
 
 
class UsersRepository(BaseRepository):
    """"
    All database actions associated with the Cleaning resource
    """
 
    async def create_users(self, *, new_user: UsersCreate) -> UsersInDB:
        query_values = new_user.dict()
        cleaning = await self.db.fetch_one(query=CREATE_USERS_QUERY, values=query_values)
 
        return UsersInDB(**cleaning)
 
 