from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies.database import get_db
from dependencies.auth import oauth2_scheme
from services.auth import JWT_SECRET_KEY
from jose import jwt
from models.user import User as user_model
from schemas.user import User as user_schema


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
):
    """
    Returns:
        schemas.user.User: userスキーマ
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        user = db.query(user_model).get(payload["id"])
    except BaseException:
        raise HTTPException(status_code=401, detail="Invalid Email or Password")

    return user_schema.from_orm(user)
