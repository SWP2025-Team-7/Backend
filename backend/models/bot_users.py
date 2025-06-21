"""
|ID|alias|login date|login time|last used date|las used time|
---------------------------------------------
|1 |@Bom |2025-02-01|   15:34  |2025-02-01    |     15:34   |
"""
from backend.models.core.core import CoreModel, IDModel
from typing import Optional
from enum import Enum
from datetime import date, time

class BotUsersBase(CoreModel):
    alias: Optional[str]
    login_date: Optional[date]
    login_time: Optional[time]
    last_used_date: Optional[date]
    last_used_time: Optional[time]

class BotUsersCreate(CoreModel):
    alias: str
    login_date: date
    login_time: time
    last_used_date: date
    last_used_time: time

class BotUsersUpdate(CoreModel):
    last_used_date: date
    last_used_time: time

class BotUsersInDB(IDModel, CoreModel):
    alias: str
    login_date: date
    login_time: time
    last_used_date: date
    last_used_time: time

class BotUsersPublic(CoreModel):
    pass
