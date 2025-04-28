from pydantic import BaseModel
from datetime import datetime
class TransactionsBase(BaseModel):
    amount: float
    description:str | None = None
    date: datetime | None = None
    category_id: int

class TransactionCreate(TransactionsBase):
    pass
class TransactionRead(TransactionsBase):
    id: int
    user_id:int

    model_config = {'from_attributes':True}

class TransactionUpdate(TransactionsBase):
    amount: float
    description: str | None = None
    date: datetime
    category_id: int

