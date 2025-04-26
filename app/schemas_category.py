from enum import Enum

from pydantic import BaseModel


class CategoryType(str, Enum):
    INCOME = 'INCOME'
    EXPENSE = 'EXPENSE'


class CategoryBase(BaseModel):
    name:str
    type:CategoryType


class CategoryCreate(CategoryBase):
    pass


class CategoryRead(CategoryBase):
    id:int
    user_id:int

    model_config = {'from_attributes': True}
