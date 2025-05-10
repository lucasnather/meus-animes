from src.model.entities import User
from pydantic import BaseModel
from sqlmodel import select
from src.model.connection import DatabaseConnection

class FindUserByIdService:

    def __init__(self, connection: DatabaseConnection) -> None:
        self.connection = connection.create_session()

    def handle(self, id: int):

        with self.connection as session:
            statement = select(User).where(User.id == id)
            find_user = session.exec(statement).first()

            if find_user is None:
                raise BaseException("User not Found")
            
            return {
                "data": {
                    "id": find_user.id,
                    "name": find_user.name,
                    "email": find_user.email,
                    "username": find_user.username,
                }
            }
