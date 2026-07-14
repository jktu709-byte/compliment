from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers.compliments import compl_router
from src.core.database import init_db
#import uvicorn

@asynccontextmanager
# Засунуть сюда функционал инициализации бд
async def app_lifespan(app:FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan= app_lifespan)
app.add_middleware(CORSMiddleware,allow_origins = "*")
app.include_router(router=compl_router)
 
