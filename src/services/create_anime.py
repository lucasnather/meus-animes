from pydantic import BaseModel
from sqlmodel import select
from src.model.connection import DatabaseConnection
from src.model.connection import User, Animes

class CreateAnimeRequest(BaseModel):
    name: str
    episodes: int
    streaming: str
    genre: str

class CreateAnimeService:

    def __init__(self, connection: DatabaseConnection) -> None:
        self.connection = connection.create_session()

    def handle(self, request: CreateAnimeRequest, user_id: int):
        with self.connection as session:
            statement = select(User).where(User.id == user_id)
            find_user = session.exec(statement).first()

            if find_user is None:
                raise BaseException("User not found")
            
            statement_anime = select(Animes).where(Animes.name == request.name)
            find_anime = session.exec(statement_anime).first()

            if find_anime is not None:
                raise BaseException("Anime already exist")
            
            anime = Animes(
                name=request.name,
                episodes=request.episodes,
                streaming=request.streaming,
                genre=request.genre,
                user_id=user_id,
            )
            session.add(anime)
            session.commit()

            return {
                "data": {
                    "name":anime.name,
                    "episodes":anime.episodes,
                    "streaming":anime.streaming,
                    "genre":anime.genre,
                    "user_id":anime.user_id,
                }
            }

            


