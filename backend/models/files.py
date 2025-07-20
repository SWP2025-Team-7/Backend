from typing import Optional
from enum import Enum
from datetime import date, time
 
from backend.models.core import CoreModel

from pydantic import BaseModel, field_serializer

class FilesExtract(BaseModel):
    file_path: str
 
class FilesExtractOutput(BaseModel):
    fullName: str
    position: str
    salary: int
    startDate: str
    company: str
    authenticity: str
    authenticityConfidence: float

class FilesExtractResponse(BaseModel):
    output: Optional[FilesExtractOutput]

class File_Type(str, Enum):
    two_ndfl = "2-ndfl"
    working_reference = "working-reference"
    resume = "resume"
    
class FilesBase(CoreModel):
    id: Optional[int]
    file_name: Optional[str]
    file_path: Optional[str]
    file_type: Optional[File_Type]
    user_id: Optional[int]
    created_at: Optional[date]
    
class FilesCreate(CoreModel):
    file_name: str
    file_path: str
    file_type: File_Type
    user_id: int
    created_at: date
    
class FilesInDB(FilesBase):
    @field_serializer("created_at") 
    def serialize_dates(self, value: date | None) -> str | None:
        return value.isoformat() if value else None
    pass

class FilesPublic(FilesBase):
    pass