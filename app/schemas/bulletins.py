from datetime import datetime
from pydantic import BaseModel

class BulletinSchema(BaseModel):
    # id: int
    name: str
    description: str
    #created_at: datetime
    type: str
    #author: str = 'test'

class BulletinTypeSchema(BaseModel):
    id: int
    name: str

class BulletinSchemaOut(BaseModel):
    id: int
    name: str
    description: str
    created_at: datetime
    type: int
    author_id: int
