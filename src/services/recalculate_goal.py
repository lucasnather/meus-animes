from src.model.connection import DatabaseConnection
from src.model.entities import User, Animes, Goals
from math import ceil
from pydantic import BaseModel
from sqlmodel import select

class RecalculateGoalRequest(BaseModel):
    episodes_watched: int
    episodes_per_day: int

class RecalculateGoalService:
    def __init__(self, connection: DatabaseConnection):
        self.connection = connection.create_session()

    def handle(self, request: RecalculateGoalRequest, user_id: int, anime_id: int, goal_id: int):
        with self.connection as session:
            statement = select(User).where(User.id == user_id)
            find_user = session.exec(statement).first()

            if not find_user:
                raise BaseException('User not found')
            
            statement_anime = select(Animes).where(Animes.id == anime_id)
            find_anime = session.exec(statement_anime).first()

            if not find_anime:
                raise BaseException('Anime not found')
            
            episodes_already_seen = find_anime.episodes - request.episodes_watched
            days_to_finish = ceil(episodes_already_seen /  request.episodes_per_day)
            
            statement_goal = select(Goals).where(Goals.id == goal_id)
            find_goal = session.exec(statement_goal).first()

            if not find_goal:
                raise BaseException('Goal not found')
            
            find_goal.episodes_per_day = request.episodes_per_day
            find_goal.episodes_watched = request.episodes_watched
            find_goal.days_to_finish_initial = days_to_finish

            session.add(find_goal)
            session.commit()
            session.refresh(find_goal)

            return {
                'data': {
                    "name":find_anime.name,
                    "episodes_per_day":request.episodes_per_day,
                    "episodes_to_finish":episodes_already_seen,
                    "days_to_finish": days_to_finish
                }
            }