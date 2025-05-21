from fastapi import FastAPI, Body, Depends, Request
from typing import Annotated
from contextlib import asynccontextmanager
from src.model.connection import DatabaseConnection
from src.adapter.password_hash import PasswordHash
from src.adapter.jwt import Jwt
from src.services.create_user import CreateUserModel, CreateUserService
from src.services.find_user_by_id import FindUserByIdService
from src.services.create_anime import CreateAnimeRequest, CreateAnimeService
from src.services.find_animes_by_user_id import FindAnimesByUserIdService
from src.services.login import LoginService, LoginRequest
from src.services.find_user import FindUserService
from src.services.create_goal import CreateGoalService ,CreateGoalRequest
from src.services.find_goals_by_user_id import FindGoalsByUserIdService
from src.services.recalculate_goal import RecalculateGoalService, RecalculateGoalRequest
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


@app.get("/users/protected", dependencies=[Depends(JWTBearer())])
def get_user_by_id(request: Request):
    try:
        id =  request.state.sub
        find_user = FindUserByIdService(connection)
        find_user_data = find_user.handle(id)

        return find_user_data
    except BaseException as e:
        return {
            "error": str(e)
        }
    
@app.post("/animes", dependencies=[Depends(JWTBearer())])
def create_animes(animes: Annotated[CreateAnimeRequest, Body()], request: Request):
    try:
        user_id = request.state.sub
        create_anime = CreateAnimeService(connection)
        anime_data = create_anime.handle(animes, user_id)

        return anime_data
    except BaseException as e:
        return {
            "error": str(e)
        }
    
@app.get("/animes", dependencies=[Depends(JWTBearer())])
def get_anime_by_user_id(request: Request):
    try:
        user_id = request.state.sub
        find_anime = FindAnimesByUserIdService(connection)
        find_anime_data = find_anime.handle(user_id)

        return find_anime_data
    except BaseException as e:
        return {
            "error": str(e)
        }
    
@app.post('/goals/{anime_id}', dependencies=[Depends(JWTBearer())])
def create_goal(anime_id: int, request: Request, body: Annotated[CreateGoalRequest, Body()]):
    try:
        user_id = request.state.sub
        create_goal = CreateGoalService(connection)
        create_goal_data = create_goal.handle(body, user_id, anime_id)

        return create_goal_data
    except BaseException as e:
        return {
            'error': str(e)
        }
    
@app.put('/goals/{anime_id}/update/{goal_id}', dependencies=[Depends(JWTBearer())])
def create_goal(anime_id: int, goal_id: int, request: Request, body: Annotated[RecalculateGoalRequest, Body()]):
    try:
        user_id = request.state.sub
        recalculate_goal = RecalculateGoalService(connection)
        recalculate_goal_data = recalculate_goal.handle(body, user_id, anime_id, goal_id)

        return recalculate_goal_data
    except BaseException as e:
        return {
            'error': str(e)
        }
    
    
@app.get("/goals", dependencies=[Depends(JWTBearer())])
def get_goals_by_user_id(request: Request):
    try:
        user_id = request.state.sub
        find_goals = FindGoalsByUserIdService(connection)
        find_goals_data = find_goals.handle(user_id)

        return find_goals_data
    except BaseException as e:
        return {
            "error": str(e)
        }
    

    

   
   