from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schemas.player import PlayerCreate, PlayerUpdate, Player
from app.services.player import PlayerService
from app.database import get_db
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/players", tags=["players"])

@router.post("/", response_model=Player)
def create_player(
    player: PlayerCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user) 
):
    player_service = PlayerService(db)
    return player_service.create_player(player, current_user)

@router.get("/", response_model=list[Player])
def read_players(db: Session = Depends(get_db)):
    player_service = PlayerService(db)
    return player_service.get_all_players()

@router.get("/{player_id}", response_model=Player)
def read_player(player_id: int, db: Session = Depends(get_db)):
    player_service = PlayerService(db)
    db_player = player_service.get_player(player_id)
    if db_player is None:
        raise HTTPException(status_code=404, detail="Player not found")
    return db_player

@router.put("/{player_id}", response_model=Player)
def update_player(
    player_id: int, 
    player: PlayerUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    player_service = PlayerService(db)
    return player_service.update_player(player, player_id, current_user)

@router.delete("/{player_id}", response_model=Player)
def delete_player(
    player_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    player_service = PlayerService(db)
    return player_service.delete_player(player_id, current_user)