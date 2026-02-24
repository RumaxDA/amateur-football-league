from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    date_of_match = Column(Date, nullable=True)
    result = Column(String, nullable=True)
    

    # Relationship with the home team
    team_1_id = Column(Integer, ForeignKey("teams.id"))
    team_1 = relationship("Team", foreign_keys=[team_1_id], back_populates="matches_as_home")

    # Relationship with the guest team
    team_2_id = Column(Integer, ForeignKey("teams.id"))
    team_2 = relationship("Team", foreign_keys=[team_2_id], back_populates="matches_as_guest")

    # Relationship with the tournament
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))
    tournament = relationship("Tournament", back_populates="matches")

    # Relationship with actions
    actions = relationship("Action", back_populates="matches")