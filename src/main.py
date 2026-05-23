from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import router
from src.core.database import init_db
import uvicorn

@asynccontextmanager
# Засунуть сюда функционал инициализации бд
async def app_lifespan():
    await init_db()
    yield

app = FastAPI(lifespan= app_lifespan)
app.add_middleware(CORSMiddleware,allow_origins = "*")
app.include_router(router=router)
 
if __name__ == "__main__":
    uvicorn.run(app="src/main:app", reload= True, host= "localhost") 