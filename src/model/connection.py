from sqlmodel import create_engine, SQLModel, Session
from src.model.entities import User, Animes, Goals

class DatabaseConnection:

    def __init__(self) -> None:
        self.url_connection = "mysql+pymysql://natherzito:teste@localhost:3306/animes"
        self.engine = None

    def create_engine_mysql(self):
        try:
            self.engine = create_engine(self.url_connection, echo=True)
            print("✅ Engine criada com sucesso!")
        except Exception as e:
            print(f"❌ Falha ao criar engine: {e}")
            raise

    def create_tables(self):
        SQLModel.metadata.create_all(self.engine)

    def create_session(self) -> Session:
        return Session(self.engine)