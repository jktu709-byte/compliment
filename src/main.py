from contextlib import asynccontextmanager
from fastapi import FastAPI
from redis.asyncio import Redis
from src.exceptions.handlers import app_error_hadler
from src.exceptions.semantic_exceptions import AppError
from src.routers.auth_router import auth_router
from src.routers.compliments_router import compl_router
from src.routers.users_router import user_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    async with Redis(host="redis",port = 6379) as client:
        app.state.redis = client
        yield
    
app = FastAPI(lifespan=lifespan)
app.add_exception_handler(AppError,app_error_hadler)  # type: ignore
# app.add_middleware(CORSMiddleware,allow_origins = "*")
# объединяем весь функционал в один большой пласт
app.include_router(router=compl_router)
app.include_router(router=user_router)
app.include_router(router=auth_router) 
