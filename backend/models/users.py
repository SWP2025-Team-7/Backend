from typing import Optional
from enum import Enum
from datetime import date, time
 
from backend.models.core import IDModel, CoreModel
 
 
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
    mail: Optional[str]
    name: Optional[str]
    surname: Optional[str]
    patronymic: Optional[str]
    phone_number: Optional[int]
    citizens: Optional[str]
    duty_to_work: Optional[Duty_To_Work] = "yes"
    duty_status: Optional[Duty_Status] = "do_not_get_in_touch"
    grant_amount: Optional[int]
    duty_period: Optional[int]
    company: Optional[str]
    resume_path: Optional[str]
    position: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    salary: Optional[int]
    working_reference_path: Optional[str]
    ndfl1_path: Optional[str]
    ndfl2_path: Optional[str]
    ndfl3_path: Optional[str]
    ndfl4_path: Optional[str]
 
 
class UsersCreate(UsersBase):
    user_id: int
    alias: str
    mail: str
    name: str
    surname: str
    patronymic: str
    # phone_number: str
    # citizens: str
    # duty_to_work: Duty_To_Work
    
 
 
class UsersUpdate(UsersBase):
    alias: Optional[str]
    mail: Optional[str]
    name: Optional[str]
    surname: Optional[str]
    patronymic: Optional[str]
    phone_number: Optional[int]
    citizens: Optional[str]
    duty_to_work: Optional[Duty_To_Work] = "yes"
    duty_status: Optional[Duty_Status] = "do_not_get_in_touch"
    grant_amount: Optional[int]
    duty_period: Optional[int]
    company: Optional[str]
    resume_path: Optional[str]
    position: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    salary: Optional[int]
    working_reference_path: Optional[str]
    ndfl1_path: Optional[str]
    ndfl2_path: Optional[str]
    ndfl3_path: Optional[str]
    ndfl4_path: Optional[str]
 
 
class UsersInDB(IDModel, UsersBase):
    pass
 
 
class UsersPublic(IDModel, UsersBase):
    pass
 
 