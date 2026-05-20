# This is something like DTO, naybe transport stuff
# Think about addresses 
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text #noqa
from src.schemas.comp_schemas import ComplimentSchema,ComplimentResponse,ComplimentHistoryResponse #noqa
from src.api.service import ComplimentService
from src.utils.depends import get_service
from src.decorators.test_conn_deco import require_db_conn

router = APIRouter(prefix="/compliments",
                   tags=["Comliments"])

@router.get("/test")
@require_db_conn
async def test_db():
    return {"msg":"Everything's ok"}
#  what should response system if db is empty? 204 - no content
@router.get("/random/{user_id}",response_model=ComplimentResponse)
async def get_user_compliment(user_id:int,service:ComplimentService = Depends(get_service)):
    ans = await service.get_compliment_for_user(user_id)
    if ans is None:
        raise HTTPException(status_code = 204, detail= "No compliments")
    return ans
# payload  = put,post    
@router.put("/{compliment_id}")
async def update_compliment(compliment_id:int,payload:ComplimentSchema,service:ComplimentService = Depends(get_service)):
    res = await service.change_compliment(compliment_id,payload)
    if res is None:
        raise HTTPException(status_code=404, detail="This compliment doesn't exist")
    return 

@router.get("/history/{user_id}",response_model=ComplimentHistoryResponse)
async def get_user_history(user_id:int,service:ComplimentService = Depends(get_service)):
    res = await service.get_history(user_id=user_id)
    if res is None:
        raise HTTPException(status_code= 204, detail="History is empty")
    return res