from sqlmodel import select
from src.model.connection import DatabaseConnection
from src.model.entities import Animes

class FindAnimesByUserIdService:

    def __init__(self, connection: DatabaseConnection) -> None:
        self.connection = connection.create_session()

    def handle(self, user_id: int):
        with self.connection as session:
            statement = select(Animes).where(Animes.user_id == user_id)
            find_animes = session.exec(statement).all()

            return {
                "data": find_animes
            }

                
            
