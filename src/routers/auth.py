from fastapi import APIRouter
from src.api.service import ComplimentService
auth_router = APIRouter(prefix="/auth",tags=["Auth"])

@auth_router.get("/me")
def get_current_status(us_id:int,service:ComplimentService,):
    service.check_my_status(user_id=us_id)