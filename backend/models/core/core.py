from pydantic import BaseModel

class CoreModel(BaseModel):
    pass

class IDModel(BaseModel):
    id: int