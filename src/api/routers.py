# This is something like DTO, naybe transport stuff
# Think about addresses 
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy import text #noqa
from src.schemas.comp_schemas import ComplimentListResponse,ComplimentHistoryResponse,ComplimentResponse#noqa
from src.api.service import ComplimentService
from src.utils.depends import get_service
from src.decorators.test_conn_deco import require_db_conn

router = APIRouter(prefix="/compliments",
                   tags=["Comliments"])

@router.get("/test")
@require_db_conn
async def test_db():
    return {"msg":"Everything's ok"}

@router.post("/data/input")
async def append_data(
    json_file:UploadFile = File(...),
    service:ComplimentService = Depends(get_service)
    ):
    try:    
        res = await service.input_data_from_file(json_file)
    except Exception as e:
        if e:
            print(f"Ошибка получена {e.__class__}")
        if not e:
            print("Всё прошло отлично")
    return res

#  what should response system if db is empty? 204 - no content
@router.get("/data/random/{user_id}",response_model=ComplimentResponse)
async def get_user_compliment(user_id:int,service:ComplimentService = Depends(get_service)):

    ans = await service.get_compliment_for_user(user_id)
    if ans is None:
        raise HTTPException(status_code = 204, detail= "No compliments")
    return ans

@router.get("/data/all",response_model= ComplimentListResponse)
async def compliments_list(service: ComplimentService):
    res = await service.list_compliments()
    return res
# payload  = put,post   
@router.put("/data/{compliment_id}")
async def update_compliment(compliment_id:int,service:ComplimentService = Depends(get_service)):
    res = await service.change_compliment(compliment_id)
    if res is None:
        raise HTTPException(status_code=404, detail="This compliment doesn't exist")
    return 

@router.get("/history/{user_id}",response_model=ComplimentHistoryResponse)
async def get_user_history(user_id:int,service:ComplimentService = Depends(get_service)):
    res = await service.get_history(user_id=user_id)
    if res is None:
        raise HTTPException(status_code= 204, detail="History is empty")
    return res