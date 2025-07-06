"""
|ID|alias|login date|login time|last used date|last used time|
---------------------------------------------
|1 |@Bom |2025-02-01|   15:34  |2025-02-01    |     15:34   |
"""
from backend.models.core.core import CoreModel, IDModel
from typing import Optional
from datetime import date, time

class BotUsersBase(CoreModel):
    user_id: Optional[int]
    username: Optional[str]
    login_date: Optional[date]
    login_time: Optional[time]
    last_used_date: Optional[date]
    last_used_time: Optional[time]

class BotUsersCreate(CoreModel):
    user_id: int
    username: str

class BotUsersUpdate(CoreModel):
    last_used_date: date
    last_used_time: time

class BotUsersInDB(IDModel, CoreModel):
    user_id: int
    username: str
    login_date: date
    login_time: time
    last_used_date: date
    last_used_time: time

class BotUsersPublic(IDModel, BotUsersBase):
    pass
