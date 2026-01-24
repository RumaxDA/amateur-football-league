from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate
from app.models import user as models
from app.utils.auth import pwd_context
from fastapi import HTTPException


def create_user(db: Session, user: UserCreate):
    hashed_pwd = pwd_context.hash(user.password)
    user.password = hashed_pwd
    user_dict = user.dict()
    db_user = models.User(**user_dict)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_all_users(db: Session):
    return db.query(models.User).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def update_user(db: Session, user: UserUpdate, user_id: int):
    db_user = get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    db.query(models.User).filter(models.User.id == user_id).update(user.dict())
    db.commit()
    return get_user(db=db, user_id=user_id)

def delete_user(db: Session, user_id: int):
    # Download the user by ID along with the assigned team
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Delete user
    db.delete(db_user)
    db.commit()

    return {"detail": "User deleted successfully"}

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.password):
        return False
    return user