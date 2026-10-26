from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  #noqa
from src.exceptions.handlers import app_error_hadler
from src.exceptions.semantic_exceptions import AppError
from src.routers.auth_router import auth_router
from src.routers.compliments_router import compl_router
from src.routers.users_router import user_router

app = FastAPI()
app.add_exception_handler(AppError,app_error_hadler)  # type: ignore
# app.add_middleware(CORSMiddleware,allow_origins = "*")
# объединяем весь функционал в один большой пласт
app.include_router(router=compl_router)
app.include_router(router=user_router)
app.include_router(router=auth_router) 
