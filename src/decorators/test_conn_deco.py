from src.tests.health import check_db_conn
from fastapi import HTTPException
from functools import wraps
from typing import Callable,Awaitable,Any

def require_db_conn(func:Callable[...,Awaitable[Any]]):
    @wraps(func)
    async def wrapper(*args,**kwargs):
        
        connection = await check_db_conn()
        if not connection:
            raise HTTPException(status_code=503, detail="Database not available")
        print ("Database is ok")
    
        res = await func(*args,**kwargs)
        return res 
    return wrapper
