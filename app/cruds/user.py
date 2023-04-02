from sqlalchemy.orm import Session
from schemas.user import UserCreate as user_create_schema
from models.user import User as user_model
from passlib import hash


def get_user_by_id(id: int, db: Session):
    user = db.query(user_model).filter(user_model.id == id).first()

    return user


def create_user(user: user_create_schema, db: Session):
    new_user = user_model(
        name=user.name, hashed_password=hash.bcrypt.hash(user.hashed_password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
