from typing import Optional
from enum import Enum
from datetime import date, time
 
from backend.models.core import CoreModel

from pydantic import BaseModel, field_serializer
 
 
class Duty_To_Work(str, Enum):
    yes = "yes"
    no = "no"
    delay = "delay"
    
class Duty_Status(str, Enum):
    working = "working"
    searching = "searching"
    not_have_to = "not_have_to"
    academ = "academ"
    army = "army"
    education = "education"
    do_nothing = "do_nothing"
    do_not_get_in_touch = "do_not_get_in_touch"
 
 
class UsersBase(CoreModel):
    user_id: Optional[int]
    alias: Optional[str]
    mail: Optional[str] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    phone_number: Optional[str] = None
    citizens: Optional[str] = None
    duty_to_work: Optional[Duty_To_Work] = None
    duty_status: Optional[Duty_Status] = None
    grant_amount: Optional[int] = None
    duty_period: Optional[int] = None
    company: Optional[str] = None
    position: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    salary: Optional[int] = None

class UsersCreate(UsersBase):
    user_id: int
    alias: str

# class UsersCreate(CoreModel):
#     user_id: int
#     alias: str
#     mail: str
#     name: str
#     surname: str
#     patronymic: str
#     # phone_number: str
#     # citizens: str
#     # duty_to_work: Duty_To_Work
    
 
 
class UsersUpdate(UsersBase):
    user_id: int = None
    alias: Optional[str] = None
 
 
class UsersInDB(UsersBase):
    @field_serializer("start_date", "end_date")
    def serialize_dates(self, value: date | None) -> str | None:
        return value.isoformat() if value else None
    pass
 
 
class UsersPublic(UsersBase):
    pass

class UsersDocumentUpload(BaseModel):
    file_path: str
 
class UsersDocumentUploadOutput(BaseModel):
    fullName: str
    position: str
    salary: int
    startDate: str
    company: str
    authenticity: str
    authenticityConfidence: float

class UsersDocumentUploadResponse(BaseModel):
    output: Optional[UsersDocumentUploadOutput]
