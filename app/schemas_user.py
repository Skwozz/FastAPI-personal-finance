from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

    model_config = {'from_attributes': True}

class Token(BaseModel):
    access_token:str
    token_type:str