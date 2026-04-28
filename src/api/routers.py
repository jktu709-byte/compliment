# This is something like DTO, naybe transport stuff  
from fastapi import APIRouter, Depends #noqa
from src.schemas.comp_schemas import ComplimentSchema,Comliment_id_schema #noqa
from src.core.database import get_session #noqa
from src.api.service import ComplimentService

router = APIRouter(prefix="/compliments",
                   tags=["Comliments"])
class Routes():
    @router.get("/test")
    async def test():
        return {"msg":"Everything ok"}
    # Think about address
    # Write service, then router 
    @router.get("/compliments/random/{user_id}")
    async def get_compliment_for_user(user_id,service:ComplimentService,session = Depends):
        return await service.get_compliment_for_user(user_id)
    
    @router.put("/compliments/{compliment_id}")
    async def update_compliment_endpoint(compliment_id:int,payload:ComplimentSchema,service:ComplimentService,):
        return await service.change_compliment()