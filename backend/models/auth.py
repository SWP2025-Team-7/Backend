from typing import Optional
from enum import Enum
from datetime import date, time
 
from backend.models.core import CoreModel

from pydantic import BaseModel, field_serializer

class Login(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str