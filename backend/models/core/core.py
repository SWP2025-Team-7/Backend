from pydantic import BaseModel

class CoreModel(BaseModel):
    class Config:
        use_enum_values = True

class IDModel(BaseModel):
    id: int