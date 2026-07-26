from fastapi import APIRouter
from src.api.service import ComplimentService #noqa
auth_router = APIRouter(prefix="/auth",tags=["Auth"])

@auth_router.get("/me")
async def about_me():
    ...

@auth_router.get("/login")
async def login():
    ...