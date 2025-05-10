from src.model.entities import User
from sqlmodel import select
from pydantic import BaseModel
from src.model.connection import DatabaseConnection
from src.adapter.password_hash import PasswordHash

class CreateUserModel(BaseModel):
    email: str
    name: str
    username: str
    password: str

class CreateUserService:

    def __init__(self, db_connection: DatabaseConnection, passwordEncoder: PasswordHash) -> None:
        self.db_connection = db_connection.create_session()
        self.password_encoder = passwordEncoder

    def handle(self, request: CreateUserModel):
       with self.db_connection as session:
    
            statement = select(User).where(User.email == request.email)
            find_user = session.exec(statement).first()

            if find_user is not None:
                raise BaseException("Email Duplicate")

            password_hash = self.password_encoder.hash_password(request.password)

            user = User(name=request.name, email=request.email, username=request.username, password=password_hash)
            session.add(user)
            session.commit()

            return {
                "data": {
                    "id": user.id,
                    "name": user.name,
                    "username": user.username,
                    "email": user.email,
                    "password": password_hash,
                }
            }