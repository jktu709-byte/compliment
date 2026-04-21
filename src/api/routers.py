# This is something like DTO, naybe transport stuff  
from fastapi import APIRouter, Depends
from src.schemas.schemas import ComplimentSchema
from src.api.crud import ComplimentRepository
from src.core.database import get_session

router = APIRouter(prefix="/compliments",
                   tags=["Comliments"])

@router.get("/test")
async def test():
    return {"msg":"Everything ok"}
# Think about address
# Write service, then router 
@router.get("/compliments/")
async def get_compliment():
    pass
 
@router.put("/compliments/{compliment_id}")
async def update_compliment_endpoint(compliment_id:int,payload:ComplimentSchema,service:ComplimentRepository = Depends(get_session)):
    return await service.update_compliment(compliment_id,payload)