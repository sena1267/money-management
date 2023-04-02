from sqlalchemy.orm import Session

from schemas.user import User as user_schema
from schemas.transaction import Transaction as tx_schema
from schemas.transaction import TransactionCreateLending as tx_create_lending_schema
from models.transaction import Transaction as tx_model


def get_lending_transactions(user: user_schema, db: Session):
    """
    Args:
        user (schemas.user.User): userスキーマ
        db (Session): Session

    Returns:
        schemas.transaction.Transaction
    """
    transactions = db.query(tx_model).filter_by(lender_id=user.id)

    return list(map(tx_schema.from_orm, transactions))


def get_borrowing_transactions(user: user_schema, db: Session):
    """
    Args:
        user (schemas.user.User): userスキーマ
        db (Session): Session

    Returns:
        schemas.transaction.Transaction
    """
    transactions = db.query(tx_model).filter_by(borrower_id=user.id)

    return list(map(tx_schema.from_orm, transactions))


def create_lending(
    user: user_schema, transaction: tx_create_lending_schema, db: Session
):
    """
    Args:
        user (schemas.user.User): userスキーマ
        db (Session): Session

    Returns:
        schemas.transaction.TransactionCreate
    """
    lending = tx_model(**transaction.dict(), lender_id=user.id)
    db.add(lending)
    db.commit()
    db.refresh(lending)

    # print(tx_schema.from_orm(lending))
    return tx_schema.from_orm(lending)
