from typing import Optional
from enum import Enum
from datetime import date, time
 
from backend.models.core import CoreModel

from pydantic import BaseModel, field_serializer

class LoginResponse(BaseModel):
    token: str