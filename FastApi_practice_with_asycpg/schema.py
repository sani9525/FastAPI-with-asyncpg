from pydantic import BaseModel,EmailStr

class Res_model(BaseModel):
    name: str
    email: EmailStr


class User(Res_model):
    password: str


class Update_user(BaseModel):
    name: str
    password:str


class search_by_id(BaseModel):
    email:EmailStr