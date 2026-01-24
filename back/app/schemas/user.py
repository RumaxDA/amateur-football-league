from pydantic import BaseModel, Field
from typing import Optional, List
from app.schemas.team import Team
from pydantic import validator
import re
from app.schemas.tournament import TournamentPlayerDisplay
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    @validator('password')
    def validate_password(cls, v):
        if not re.search(r'(?=.*[A-Z])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*\d).{8,}', v):
            raise ValueError('Hasło jest za słabe...')
        return v

class UserUpdate(UserBase):
    pass

class UserLogin(BaseModel):
    email: str
    password: str

class UserChangePassword(BaseModel):
    password: str
    new_password: str
    confirm_new_password: str
    
    @validator('new_password')
    def validate_password(cls, v):
        if not re.search(r'(?=.*[A-Z])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*\d).{8,}', v):
            raise ValueError('Hasło jest za słabe...')
        return v

class User(BaseModel):
    id: int
    username: str
    email: str
    team: Optional[Team] = None
    is_superuser: bool
    is_referee: bool
    tournaments: Optional[List[TournamentPlayerDisplay]] = None

    class Config:
        from_attribues = True
