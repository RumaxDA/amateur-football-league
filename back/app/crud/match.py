from sqlalchemy.orm import Session
from app.schemas.match import MatchCreate, MatchUpdate, Match
from app.models import match as models
from app.models import team as team_models
from app.models import tournament as tournament_models
from fastapi import HTTPException
from app.models.match import Match
from app.models.action import Action, ActionTypeEnum
from app.crud.tournament import check_and_update_tournament_status



def increment_matches_played(db: Session, team_ids: list[int]):
    teams = db.query(team_models.Team).filter(team_models.Team.id.in_(team_ids)).all()
    for team in teams:
        team.matches_played = (team.matches_played or 0) + 1

def create_match(db: Session, match: MatchCreate):
    db_tournament = db.query(tournament_models.Tournament).get(match.tournament_id)
    if not db_tournament:
        raise HTTPException(status_code=400, detail="Tournament not found")
    
    db_match = Match(**match.dict())
    with db.begin(): 
        db.add(db_match)
        db.flush() 
        if db_match.result is not None:
            increment_matches_played(db, [db_match.team_1_id, db_match.team_2_id])
    db.refresh(db_match)
    return db_match

def get_all_matches(db: Session):
    return db.query(models.Match).all()

def get_matches_with_results(db: Session):
    return db.query(models.Match).filter(models.Match.result != None).all()

def get_match(db: Session, match_id: int):
    return db.query(models.Match).filter(models.Match.id == match_id).first()

def update_match(db: Session, match_data: MatchUpdate, match_id: int):
    db_match = db.query(Match).filter(Match.id == match_id).first()
    if not db_match:
        return None

    for key, value in match_data.dict(exclude_unset=True).items():
        setattr(db_match, key, value)
    db.commit()
    db.refresh(db_match)
    return db_match

def delete_match(db: Session, match_id: int):
    db_match = get_match(db=db, match_id=match_id)
    if db_match:
        # Usuń wszystkie akcje powiązane z meczem
        db.query(Action).filter(Action.match_id == match_id).delete()
        db.commit()

        # Usuń mecz
        db.delete(db_match)
        db.commit()
    return db_match


def get_match_player(db:Session, match_id:int):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        return None
    team_1_players = match.team_1_id.players
    team_2_players = match.team_2_id.players
    return {
        "team_1_players": team_1_players,
        "team_2_players": team_2_players
    }


def calculate_match_result(db: Session, match_id: int):
    actions = db.query(Action).filter(Action.match_id == match_id).all()

    if not actions:
        return None 

    db_match = db.query(Match).filter(Match.id == match_id).first()
    if not db_match:
        return None  

    team_1_id = db_match.team_1_id
    team_2_id = db_match.team_2_id

    team_goals = {team_1_id: 0, team_2_id: 0}
    for action in actions:
        if action.action_type == ActionTypeEnum.Goal:
            if action.team_id in team_goals:
                team_goals[action.team_id] += 1

    result = f"{team_goals.get(team_1_id, 0)}:{team_goals.get(team_2_id, 0)}"

    db_match.result = result
    db.commit()
    db.refresh(db_match)

    # Update matches_played for both teams if result is not None
    if db_match.result is not None:
        team_1 = db.query(team_models.Team).filter(team_models.Team.id == db_match.team_1_id).first()
        team_2 = db.query(team_models.Team).filter(team_models.Team.id == db_match.team_2_id).first()

        if team_1:
            team_1.matches_played = team_1.matches_played + 1 if team_1.matches_played is not None else 1
        if team_2:
            team_2.matches_played = team_2.matches_played + 1 if team_2.matches_played is not None else 1

        db.commit()

    check_and_update_tournament_status(db, db_match.tournament_id)

    return db_match






