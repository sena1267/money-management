from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.user import UserCreate as user_create_schema
from schemas.user import User as user_schema
from dependencies import database
from dependencies.user import get_current_user
from services.auth import get_user_by_name
import cruds.user as user_crud

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=user_schema)
def create_user(user: user_create_schema, db: Session = Depends(database.get_db)):
    db_user = get_user_by_name(name=user.name, db=db)
    if db_user:
        raise HTTPException(status_code=400, detail="既に使われているユーザー名です。")

    new_user = user_crud.create_user(user=user, db=db)

    return user_schema.from_orm(new_user)


@router.get("/me", response_model=user_schema)
def get_user(user: user_schema = Depends(get_current_user)):
    return user
