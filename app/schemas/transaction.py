from pydantic import BaseModel
from datetime import datetime


class Transaction(BaseModel):
    id: int
    amount: int
    description: str
    lender_id: str
    borrower_id: str
    created_at: datetime

    class Config:
        orm_mode = True


class TransactionCreateLending(BaseModel):
    amount: int
    description: str
    borrower_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TransactionCreateBorrowing(BaseModel):
    amount: int
    description: str
    borrower_id: int
    created_at: datetime

    class Config:
        orm_mode = True
