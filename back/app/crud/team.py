from sqlalchemy.orm import Session
from app.schemas.team import TeamCreate, TeamUpdate
from app.models import team as models
from sqlalchemy.orm import joinedload

def create_team(db: Session, team: TeamCreate, creator_id: str):
    db_team = models.Team(creator_id = creator_id, **team.dict())
    db.add(db_team)
    db.commit()
    db.refresh(db_team)
    return db_team

def get_all_teams(db: Session):
    return db.query(models.Team).all()

def get_team(db: Session, team_id: int):
    return db.query(models.Team).options(joinedload(models.Team.players)).filter(models.Team.id == team_id).first()

def update_team(db: Session, team: TeamUpdate, team_id: int):
    db.query(models.Team).filter(models.Team.id == team_id).update(team.dict())
    db.commit()
    return get_team(db=db, team_id=team_id)

def delete_team(db: Session, team_id: int):
    db_team = get_team(db=db, team_id=team_id)
    db.delete(db_team)
    db.commit()
    return db_team