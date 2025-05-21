from src.model.connection import DatabaseConnection
from src.model.entities import User, Goals, Animes
from sqlmodel import select
from sqlalchemy.orm import selectinload

class FindGoalsByUserIdService:

    def __init__(self, connection: DatabaseConnection):
        self.connection = connection.create_session()

    def handle(self, user_id):
        with self.connection as session:
            statement = select(User).where(User.id == user_id)
            find_user = session.exec(statement).first()

            if not find_user:
                raise BaseException('User not exist')
            
            statement_goal = (
                select(Goals)
                .join(Goals.animes)  # faz join com a tabela de animes
                .where(Animes.user_id == user_id)
                .options(selectinload(Goals.animes))  # carrega os dados do anime junto
            )
            find_goals = session.exec(statement_goal).all()

            return {
                'data': find_goals
            }