from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session
from app.schemas.team import TeamCreate, TeamUpdate, Team
from app.services.team import TeamService
from app.database import get_db
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/teams", tags=["teams"])

@router.post("/", response_model=Team)
def create_team(
    team: TeamCreate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    team_service = TeamService(db)

    existing_team = team_service.get_team_by_user_id(current_user.id)
    if existing_team is not None:
        raise HTTPException(status_code=400, detail="User already has a team")

    return team_service.create_team(team, creator_id=current_user.id)

@router.get("/", response_model=list[Team])
def read_teams(db: Session = Depends(get_db)):
    team_service = TeamService(db)
    return team_service.get_all_teams()

@router.get("/{team_id}", response_model=Team)
def read_team(team_id: int, db: Session = Depends(get_db)):
    team_service = TeamService(db)
    db_team = team_service.get_team(team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    return db_team

@router.put("/{team_id}", response_model=Team)
def update_team(
    team_id: int, 
    team: TeamUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    team_service = TeamService(db)
    db_team = team_service.get_team(team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")
    
    if db_team.creator_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Nie możesz edytować nie swojej drużyny")

    return team_service.update_team(team, team_id)

@router.delete("/{team_id}", response_model=Team)
def delete_team(
    team_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    team_service = TeamService(db)
    db_team = team_service.get_team(team_id)
    if db_team is None:
        raise HTTPException(status_code=404, detail="Team not found")

    if db_team.creator_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Nie możesz usunąć nie swojej drużyny")

    return team_service.delete_team(team_id)