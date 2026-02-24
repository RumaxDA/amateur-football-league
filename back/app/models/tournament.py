from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date
from sqlalchemy.orm import relationship
from app.database import Base
from app.association_tables import team_tournament


class Tournament(Base):
    __tablename__ = "tournaments"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    amount_of_teams = Column(Integer)
    is_active = Column(Boolean, default=True)
    is_full = Column(Boolean, default=False)
    date_of_tournament = Column(Date, None)

    #Many-to-many relationship with teams
    teams = relationship("Team", secondary=team_tournament, back_populates="tournaments")
    
    #One-to-many relationship with matches
    matches = relationship("Match", back_populates = "tournament", cascade = "all, delete-orphan")
    creator_id = Column(Integer, ForeignKey("users.id"))
    creator = relationship("User", back_populates="tournaments")

    actions = relationship("Action", back_populates="tournaments", cascade = "all, delete-orphan")
    tournament_table = relationship("TournamentTable", back_populates="tournament", cascade="all, delete-orphan")
