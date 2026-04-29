# This is something like DTO, naybe transport stuff
# Think about addresses 
from fastapi import APIRouter, Depends #noqa
from src.schemas.comp_schemas import ComplimentSchema,Comliment_id_schema #noqa
from src.api.service import ComplimentService
from src.utils.depends import get_service

router = APIRouter(prefix="/compliments",
                   tags=["Comliments"])

@router.get("/test")

async def test():
    return {"msg":"Everything ok"}
#  what should response system if db is empty? None? 404 - not found? 204 - no content?
@router.get("/random/{user_id}")
async def get_compliment_for_user(user_id:int,service:ComplimentService = Depends(get_service)):
    return await service.get_compliment_for_user(user_id)
    
@router.put("/{compliment_id}")
async def update_compliment_endpoint(compliment_id:int,payload:ComplimentSchema,service:ComplimentService = Depends(get_service)):
    return await service.change_compliment(compliment_id)