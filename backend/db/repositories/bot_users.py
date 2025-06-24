from backend.db.repositories.base import BaseRepository
from backend.models.bot_users import BotUsersCreate, BotUsersUpdate, BotUsersInDB

CREATE_BOT_USERS_QUERY = """
    INSERT INTO bot_users (user_id, login_date, login_time, last_used_date, last_used_time)
    VALUES (:user_id, :login_date, :login_time, :last_used_date, :last_used_time)
    RETURNING id, user_id, login_date, login_time, last_used_date, last_used_time
"""

class BotUsersRepository(BaseRepository):

    async def create_bot_user(self, new_bot_user: BotUsersCreate) -> BotUsersInDB:
        query_values = new_bot_user.dict()
        bot_user = await self.db.fetch_one(query=CREATE_BOT_USERS_QUERY, values=query_values)

        return BotUsersInDB(**bot_user)