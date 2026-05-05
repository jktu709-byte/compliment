from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routers import router

app = FastAPI()
app.add_middleware(CORSMiddleware,allow_origins = "*")
app.include_router(router=router)
