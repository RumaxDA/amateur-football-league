from sqlalchemy.orm import Session
from app.schemas.tournament import TournamentCreate, TournamentUpdate
from app.models import tournament as models


def create_tournament(db: Session, tournament: TournamentCreate, creator_id: int):
    db_tournament = models.Tournament(creator_id=creator_id, **tournament.dict())
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament

def get_all_tournaments(db: Session, limit: int = None):
    query = db.query(models.Tournament)
    if limit:
        query = query.limit(limit)
    return query.all()

def get_tournament(db: Session, tournament_id: int):
    return db.query(models.Tournament).filter(models.Tournament.id == tournament_id).first()

def update_tournament(db: Session, tournament: TournamentUpdate, tournament_id: int):
    db.query(models.Tournament).filter(models.Tournament.id == tournament_id).update(tournament.dict(exclude_unset = True))
    db.commit()
    return get_tournament(db=db, tournament_id=tournament_id)

def delete_tournament(db: Session, tournament_id: int):
    db_tournament = get_tournament(db=db, tournament_id=tournament_id)
    if db_tournament:
        db.delete(db_tournament)
        db.commit()
    return db_tournament

def check_and_update_tournament_status(db: Session, tournament_id: int):
    db_tournament = get_tournament(db=db, tournament_id=tournament_id)
    if db_tournament:
        all_matches_have_result = all(result is not None and result != "" for result in db_tournament.matches)
        if all_matches_have_result:
            db_tournament.is_active = False
            db.commit()