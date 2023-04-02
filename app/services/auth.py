from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from passlib import hash
from jose import jwt
from models.user import User as user_model
from schemas.user import User as user_schema
from setting import Settings

settings = Settings()

JWT_SECRET_KEY = settings.jwt_secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def get_user_by_name(name: str, db: Session):
    return db.query(user_model).filter(user_model.name == name).first()


def authenticate_user(name: str, password: str, db: Session):
    user = get_user_by_name(name=name, db=db)

    if not user:
        return False

    if not hash.bcrypt.verify(password, user.hashed_password):
        return False

    return user


def create_token(user: user_model):
    pass
    to_encode = user_schema.from_orm(user).dict()
    print(type(to_encode))
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

    return dict(access_token=token, token_type="bearer")
