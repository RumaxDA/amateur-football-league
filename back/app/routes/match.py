from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.match import MatchCreate, MatchUpdate, Match
from app.services.match import MatchService
from app.database import get_db
from app.schemas.team import Team
from typing import Optional

router = APIRouter(prefix="/matches", tags=["matches"])

def get_match_service(db: Session = Depends(get_db)):
    return MatchService(db)

@router.post("/", response_model=Match)
def create_match(match: MatchCreate, service: MatchService = Depends(get_match_service)):
    return service.create_match(match)

@router.get("/", response_model=list[Match])
def read_matches(limit: Optional[int]= None, db: Session = Depends(get_db)):
    match_service = MatchService(db)
    return match_service.get_all_matches(limit=limit)


@router.get("/matches_with_results", response_model=list[Match])
def read_all_matches_with_results(limit: Optional[int]= None, db: Session = Depends(get_db)):
    match_service = MatchService(db)
    return match_service.get_matches_with_results(limit=limit)

@router.get("/{match_id}", response_model=Match)
def read_match(match_id: int, db: Session = Depends(get_db)):
    match_service = MatchService(db)
    db_match = match_service.get_match(match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return db_match

@router.put("/{match_id}", response_model=Match)
def update_match(match_id: int, match: MatchUpdate, db: Session = Depends(get_db)):
    match_service = MatchService(db)
    db_match = match_service.get_match(match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return match_service.update_match(match, match_id)

@router.delete("/{match_id}", response_model=Match)
def delete_match(match_id: int, db: Session = Depends(get_db)):
    match_service = MatchService(db)
    db_match = match_service.get_match(match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return match_service.delete_match(match_id)

@router.get("/{match_id}/teams", response_model=list[Team])
def read_match_teams(match_id: int, db: Session = Depends(get_db)):
    match_service = MatchService(db)
    db_match = match_service.get_match(match_id)
    if db_match is None:
        raise HTTPException(status_code=404, detail="Match not found")
    return db_match.team_1, db_match.team_2
