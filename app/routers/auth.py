from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas.auth import Token as token_schema
from dependencies import database
from services.auth import authenticate_user, create_token

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=token_schema)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    name = form_data.username
    password = form_data.password

    user = authenticate_user(name=name, password=password, db=db)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    return create_token(user=user)
