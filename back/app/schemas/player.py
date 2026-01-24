from pydantic import BaseModel, Field, validator
from datetime import date
from enum import Enum
from typing import Optional
import re

class SexEnum(str, Enum):
    Male = "Male"
    Female = "Female"

class PlayerBase(BaseModel):
    name: str
    last_name: str
    
    @validator('name')
    def validate_name(cls, v):
        if re.search(r'\d', v):
            raise ValueError("First name cannot contain numbers")
        return v

    @validator('last_name')
    def validate_last_name(cls, v):
        if re.search(r'\d', v):
            raise ValueError("Last name cannot contain numbers")
        return v

class PlayerCreate(PlayerBase):
    date_of_birth: date 
    gender: SexEnum     
    team_id: int       

    @validator('date_of_birth')
    def validate_age(cls, v):
        if not (1960 <= v.year <= 2010):
            raise ValueError("Date of birth must be between 1960 and 2010")
        return v

class PlayerUpdate(BaseModel): 
    name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[SexEnum] = None

    @validator('name')
    def validate_name(cls, v):
        if v and re.search(r'\d', v):
            raise ValueError("First name cannot contain numbers")
        return v

    @validator('last_name')
    def validate_last_name(cls, v):
        if v and re.search(r'\d', v):
            raise ValueError("Last name cannot contain numbers")
        return v
        
    @validator('date_of_birth')
    def validate_age(cls, v):
        if v and not (1980 <= v.year <= 2010):
            raise ValueError("Date of birth must be between 1980 and 2010")
        return v

class Player(PlayerBase):
    id: int
    date_of_birth: date
    gender: SexEnum
    team_id: int

    class Config:
        from_attributes = True