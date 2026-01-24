from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from app.association_tables import team_tournament

class Team(Base):
    __tablename__ = "teams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    players = relationship("Player", back_populates="team", cascade="all, delete-orphan")
    matches_played = Column(Integer)

     # Relationship with matches as home team
    matches_as_home = relationship("Match", foreign_keys="Match.team_1_id", back_populates="team_1")

    # Relationship with matches as guest team
    matches_as_guest = relationship("Match", foreign_keys="Match.team_2_id", back_populates="team_2")

    # Relationship with the creator of the team
    creator = relationship("User", back_populates="team", uselist=False)
    creator_id = Column(Integer, ForeignKey("users.id"))

     # Many-to-many relationship with tournaments
    tournaments = relationship("Tournament", secondary=team_tournament, back_populates="teams")

    # Relationship with actions
    actions = relationship("Action", back_populates="teams")

    # Relationship with tournament tables
    tournament_tables = relationship("TournamentTable", back_populates="team")

