from sqlalchemy.orm import Session
from app.schemas.player import PlayerCreate, PlayerUpdate
from app.models import player as models


def create_player(db: Session, player: PlayerCreate):
    db_player = models.Player(**player.dict())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player

def get_all_players(db: Session):
    return db.query(models.Player).all()

def get_player(db: Session, player_id: int):
    return db.query(models.Player).filter(models.Player.id == player_id).first()

def update_player(db: Session, player: PlayerUpdate, player_id: int):
    update_data = player.dict(exclude_unset=True)
    
    db.query(models.Player).filter(models.Player.id == player_id).update(update_data)
    db.commit()
    return get_player(db=db, player_id=player_id)

def delete_player(db: Session, player_id: int):
    db_player = get_player(db=db, player_id=player_id)
    db.delete(db_player)
    db.commit()
    return db_player