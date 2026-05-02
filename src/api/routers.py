# This is something like DTO, naybe transport stuff
# Think about addresses 
from fastapi import APIRouter, Depends, HTTPException #noqa
from src.schemas.comp_schemas import ComplimentSchema,ComplimentResponse #noqa
from src.api.service import ComplimentService
from src.utils.depends import get_service

router = APIRouter(prefix="/compliments",
                   tags=["Comliments"])

@router.get("/test")

async def test():
    return {"msg":"Everything ok"}
#  what should response system if db is empty? None? 404 - not found? 204 - no content?
@router.get("/random/{user_id}",response_model=ComplimentResponse)
async def get_compliment_for_user(user_id:int,service:ComplimentService = Depends(get_service)):
    ans = await service.get_compliment_for_user(user_id)
    if ans is None:
        raise HTTPException(status_code = 404, detail= "No data")
    return ans
# payload  = put,post    
@router.put("/{compliment_id}")
async def update_compliment_endpoint(compliment_id:int,payload:ComplimentSchema,service:ComplimentService = Depends(get_service)):
    return await service.change_compliment(compliment_id,payload)