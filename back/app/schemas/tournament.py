from pydantic import BaseModel, validator
from typing import List, Optional
from app.schemas.team import TeamTournamentDisplay
from datetime import date, datetime, timedelta
from app.schemas.match import MatchTournament


class TournamentBase(BaseModel):
    name: str
    amount_of_teams: int

    @validator('name')
    def validate_name(cls, v):
        if len(v) > 40:
            raise ValueError("Tournament name cannot exceed 40 characters")
        return v
class TournamentCreate(TournamentBase):
    date_of_tournament: Optional[date] = None

    @validator('date_of_tournament')
    def validate_date(cls, v):
        today = datetime.now().date()
        six_months_from_now = today + timedelta(days = 100)
        if not (today <= v <= six_months_from_now):
            raise ValueError("Tournament date must be between today and 6 month from now")
        return v
class TournamentUpdate(BaseModel):
    name: Optional[str] = None
    amount_of_teams: Optional[int] = None
    date_of_tournament: Optional[date] = None

    @validator('name')
    def validate_name(cls, v):
        if v and len(v) > 40:
            raise ValueError("Tournament name cannot exceed 40 characters")
        return v
    
    @validator('date_of_tournament')
    def validate_date(cls, v):
        if v:
            today = datetime.now().date()
            six_months_from_now = today + timedelta(days = 100)
            if not (today <= v <= six_months_from_now):
                raise ValueError("Tournament date must be between today and 6 months from now")
            return v
class AddTeamToTournament(BaseModel):
    team_id: int

class TournamentPlayerDisplay(BaseModel):
    id: int
    name: str
    is_active: bool

class Tournament(BaseModel):
    id: int
    name: str
    amount_of_teams: int
    date_of_tournament: Optional[date] = None
    teams: Optional[List[TeamTournamentDisplay]] = None
    matches: Optional[List[MatchTournament]] = None
    is_full: Optional[bool] = False
    is_active: Optional[bool] = True
    creator_id: int
    class Config:
        from_attributes = True