from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.database import init_db
from src.routers.auth import auth_router
from src.routers.compliments import compl_router
from src.routers.users import user_router


# Засунуть сюда функционал инициализации бд
@asynccontextmanager
async def app_lifespan(app:FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan= app_lifespan)
app.add_middleware(CORSMiddleware,allow_origins = "*")
app.include_router(router=compl_router)
app.include_router(router=user_router)
app.include_router(router=auth_router) 
