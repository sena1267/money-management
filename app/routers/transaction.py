from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import cruds.transaction as transaction_crud
import cruds.user as user_crud
from dependencies.user import get_current_user
from dependencies.database import get_db
from schemas.user import User as user_schema
from schemas.transaction import Transaction as transaction_schema
from schemas.transaction import TransactionCreateLending as tx_create_lending_schema

router = APIRouter(prefix="/transaction", tags=["Transactions"])


@router.get("/lending", response_model=list[transaction_schema])
def get_lending(
    user: user_schema = Depends(get_current_user), db: Session = Depends(get_db)
):
    return transaction_crud.get_lending_transactions(user=user, db=db)


@router.post("/lending")
def create_lending(
    transaction: tx_create_lending_schema,
    user: user_schema = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if transaction.borrower_id == user.id:
        raise HTTPException(status_code=400, detail="自分以外のユーザーを選択してください。")

    inserted_user = user_crud.get_user_by_id(id=transaction.borrower_id, db=db)
    if inserted_user is None:
        raise HTTPException(status_code=404, detail="存在しないユーザーです。")

    return transaction_crud.create_lending(user=user, transaction=transaction, db=db)


@router.get("/borrowing", response_model=list[transaction_schema])
def get_borrowing(
    user: user_schema = Depends(get_current_user), db: Session = Depends(get_db)
):
    return transaction_crud.get_borrowing_transactions(user=user, db=db)
