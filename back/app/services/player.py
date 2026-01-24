from app.schemas.player import PlayerCreate, PlayerUpdate
from app.models import player as models
from app.models.team import Team # Potrzebne do sprawdzenia właściciela
from app.models.user import User
from app.crud.player import create_player as crud_create, get_all_players, get_player, update_player as crud_update, delete_player as crud_delete
from sqlalchemy.orm import Session
from typing import Optional
from fastapi import HTTPException, status

class PlayerService:
    def __init__(self, db: Session):
        self.db = db

    def create_player(self, player: PlayerCreate, current_user: User) -> models.Player:
        team = self.db.query(Team).filter(Team.id == player.team_id).first()
        if not team:
            raise HTTPException(status_code=404, detail="Team not found")
        
        if team.creator_id != current_user.id and not current_user.is_superuser:
            raise HTTPException(status_code=403, detail="You can only add players to your own team")

        return crud_create(self.db, player)

    def get_all_players(self) -> list[models.Player]:
        return get_all_players(self.db)

    def get_player(self, player_id: int) -> Optional[models.Player]:
        return get_player(self.db, player_id)

    def update_player(self, player: PlayerUpdate, player_id: int, current_user: User) -> Optional[models.Player]:
        db_player = self.get_player(player_id)
        if not db_player:
            raise HTTPException(status_code=404, detail="Player not found")

        if db_player.team.creator_id != current_user.id and not current_user.is_superuser:
             raise HTTPException(status_code=403, detail="You cannot edit player from another team")

        return crud_update(self.db, player, player_id)

    def delete_player(self, player_id: int, current_user: User) -> Optional[models.Player]:
        db_player = self.get_player(player_id)
        if not db_player:
            raise HTTPException(status_code=404, detail="Player not found")

        if db_player.team.creator_id != current_user.id and not current_user.is_superuser:
             raise HTTPException(status_code=403, detail="You cannot delete player from another team")

        return crud_delete(self.db, player_id)