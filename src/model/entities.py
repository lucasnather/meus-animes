from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import List

class User(SQLModel, table=True):
    id: int = Field(primary_key=True )
    name: str
    username: str | None = Field(unique=True, nullable=True)
    email: str = Field(unique=True)
    password: str
    
    animes: List["Animes"] | None =  Relationship(back_populates="user")

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class Animes(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    episodes: int
    streaming: str
    genre: str

    user_id: int | None = Field(default=None, foreign_key="user.id")
    user: User =  Relationship(back_populates="animes")
    goals: List["Goals"] = Relationship(back_populates="animes")

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class Goals(SQLModel, table=True):
    id: int = Field(primary_key=True)
    days_to_finish: int
    episodes_watched: int
    episodes_anime: int
    episodes_per_day: int
    is_late_or_ahead: str

    animes_id: int = Field(default=None, foreign_key="animes.id")
    animes: Animes =  Relationship(back_populates="goals")

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)