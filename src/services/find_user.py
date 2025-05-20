from src.model.connection import DatabaseConnection
from src.model.entities import User
from sqlmodel import select

class FindUserService:

    def __init__(self, connection: DatabaseConnection ) -> None:
        self.connection = connection.create_session()

    def handle(self):
        with self.connection as session:
            statement = select(User)
            find_users = session.exec(statement).all()

            return {
                "data": {
                    "users": find_users
                }
            }