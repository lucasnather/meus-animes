from pydantic import BaseModel
from sqlmodel import select
from src.model.connection import DatabaseConnection
from src.model.entities import User
from src.adapter.password_hash import PasswordHash
from src.adapter.jwt import Jwt

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginService:
    
    def __init__(self, 
            connection: DatabaseConnection, 
            password_decoder: PasswordHash,
            jwt: Jwt,
        ) -> None:
        self.connection = connection.create_session()
        self.password_decoder = password_decoder
        self.jwt = jwt

    def handle(self, request: LoginRequest):
        with self.connection as session:
            statement = select(User).where(User.email == request.email)
            find_user = session.exec(statement).first()

            if find_user is None:
                raise BaseException("Invalid Credentials")
            
            compare_password = self.password_decoder.verify_password(request.password, find_user.password)

            if compare_password == False:
                raise BaseException("Invalid Credentials")
            
            data = {
                "name": find_user.name,
                "sub": str(find_user.id),
            }
            
            token = self.jwt.generate_token(data)
            
            return {
                "access_token": token
            }