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

class UserMe(UserBase):
    categories_count:int
    transactions_count:int
    income_total: float
    expense_total: float

    model_config = {'from_attributes': True}