from app.schemas.team import TeamCreate, TeamUpdate
from app.models import team as models
from app.crud.team import create_team, get_all_teams, get_team, update_team, delete_team
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import select
from fastapi import HTTPException
from app.models.team import Team

class TeamService:
    def __init__(self, db: Session):
        self.db = db

    def create_team(self, team: TeamCreate, creator_id: int) -> models.Team:
        if len(team.name) > 30:
            raise HTTPException(status_code=400, detail="Team name cannot exceed 30 characters")
        
        return create_team(self.db, team, creator_id)

    def get_all_teams(self) -> list[models.Team]:
        return get_all_teams(self.db)

    def get_team(self, team_id: int) -> Optional[models.Team]:
        return get_team(self.db, team_id)

    def update_team(self, team: TeamUpdate, team_id: int) -> Optional[models.Team]:
        if team.name and len(team.name) > 30:
            raise HTTPException(status_code=400, detail="Team name cannot exceed 30 characters")
        
        return update_team(self.db, team, team_id)

    def delete_team(self, team_id: int) -> Optional[models.Team]:
        return delete_team(self.db, team_id)

    def get_team_by_user_id(self, user_id: int) -> Optional[models.Team]:
        stmt = select(Team).where(Team.creator_id == user_id)
        result = self.db.execute(stmt)
        return result.scalars().first()
    

