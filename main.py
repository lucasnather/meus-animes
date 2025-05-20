from fastapi import FastAPI, Body, Depends
from typing import Annotated
from contextlib import asynccontextmanager
from src.model.connection import DatabaseConnection
from src.adapter.password_hash import PasswordHash
from src.adapter.jwt import Jwt
from src.services.create_user import CreateUserModel, CreateUserService
from src.services.find_user_by_id import FindUserByIdService
from src.services.create_anime import CreateAnimeRequest, CreateAnimeService
from src.services.find_animes_by_user_id import FindAnimesByUserIdService
from src.services.find_animes_by_user_id import FindAnimesByUserIdService
from src.services.login import LoginService, LoginRequest
from src.services.find_user import FindUserService
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from src.middleware.verify_token import JWTBearer

connection = DatabaseConnection()
password_hash = PasswordHash()
jwt = Jwt()

@asynccontextmanager
async def lifespan(app: FastAPI):
    connection.create_engine_mysql()
    connection.create_tables()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/users")
def create_users(users: Annotated[CreateUserModel, Body()]):
    try:
        create_user = CreateUserService(connection, password_hash)
        user_data = create_user.handle(users)

        return user_data
    except BaseException as e:
        return {
            "error": str(e)
        }
    
@app.post("/login")
def login(users: Annotated[LoginRequest, Body()]):
    try:
        login_user = LoginService(connection, password_hash, jwt)
        login_data = login_user.handle(users)

        return login_data
    except BaseException as e:
        return {
            "error": str(e)
        }
    
@app.get("/users")
def find_users():
    try:
        find_user_service = FindUserService(connection)
        user_data = find_user_service.handle()

        return user_data
    except BaseException as e:
        return {
            "error": str(e)
        }


@app.get("/users/{id}", dependencies=[Depends(JWTBearer())])
def get_user_by_id(id: int):
    try:
        find_user = FindUserByIdService(connection)
        find_user_data = find_user.handle(id)

        return find_user_data
    except BaseException as e:
        return {
            "error": str(e)
        }
    
@app.post("/animes/{user_id}")
def create_animes(animes: Annotated[CreateAnimeRequest, Body()], user_id: int):
    try:
        create_anime = CreateAnimeService(connection)
        anime_data = create_anime.handle(animes, user_id)

        return anime_data
    except BaseException as e:
        return {
            "error": str(e)
        }
    
@app.get("/animes/{user_id}")
def get_anime_by_user_id(user_id: int):
    try:
        find_anime = FindAnimesByUserIdService(connection)
        find_anime_data = find_anime.handle(user_id)

        return find_anime_data
    except BaseException as e:
        return {
            "error": str(e)
        }

    

   
   