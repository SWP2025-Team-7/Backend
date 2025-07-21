from typing import Optional
from enum import Enum
from datetime import date, time
 
from backend.models.core import CoreModel

from pydantic import BaseModel, field_serializer

class AdminsBase(CoreModel):
    username: Optional[str]
    hashed_password: Optional[str]

class AdminsCreate(CoreModel):
    username: str
    hashed_password: str
    
class AdminsInDB(CoreModel):
    id: int
    username: str
    hashed_password: str