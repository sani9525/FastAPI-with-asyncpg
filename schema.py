from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    id: int
    name: str
    email: str