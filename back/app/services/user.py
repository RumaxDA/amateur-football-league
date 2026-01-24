from app.schemas.user import UserCreate, UserUpdate
from app.models import user as models
from app.crud.user import create_user, get_all_users, get_user, update_user, delete_user, authenticate_user
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import HTTPException
from app.utils.auth import hash_password, verify_password
import re

class UserService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user: UserCreate) -> models.User:
        return create_user(self.db, user)

    def get_all_users(self) -> list[models.User]:
        return get_all_users(self.db)

    def get_user(self, user_id: int) -> Optional[models.User]:
        return get_user(self.db, user_id)

    def update_user(self, user: UserUpdate, user_id: int) -> Optional[models.User]:
        db_user = self.get_user(user_id)
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")

        return update_user(self.db, user, user_id)

    def delete_user(self, user_id: int) -> Optional[models.User]:
        return delete_user(self.db, user_id)

    def authenticate_user(self, email: str, password: str) -> Optional[models.User]:
        return authenticate_user(self.db, email, password)

    
    def change_password(self, user_id: int, password: str, new_password: str) -> Optional[models.User]:
        db_user = get_user(self.db, user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not verify_password(password, db_user.password):
            raise HTTPException(status_code=400, detail="Old password is incorrect")

        db_user.password = hash_password(new_password)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user