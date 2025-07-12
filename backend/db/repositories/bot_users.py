from backend.db.repositories.base import BaseRepository
from backend.models.bot_users import BotUsersCreate, BotUsersUpdate, BotUsersInDB
from datetime import datetime

CREATE_BOT_USERS_QUERY = """
    INSERT INTO bot_users (user_id, username, login_date, login_time, last_used_date, last_used_time)
    VALUES (:user_id, :username, :login_date, :login_time, :last_used_date, :last_used_time)
    RETURNING id, user_id, username, login_date, login_time, last_used_date, last_used_time
"""

class BotUsersRepository(BaseRepository):

    async def create_bot_user(self, new_bot_user: BotUsersCreate) -> BotUsersInDB:
        query_values = new_bot_user.dict()
        query_values['login_date'] = datetime.now().date()
        query_values['login_time'] = datetime.now().time()
        query_values['last_used_date'] = datetime.now().date()
        query_values['last_used_time'] = datetime.now().time()
        bot_user = await self.db.fetch_one(query=CREATE_BOT_USERS_QUERY, values=query_values)
        return BotUsersInDB(**bot_user)