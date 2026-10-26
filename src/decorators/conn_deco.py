from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any

from fastapi import HTTPException

from src.tests.integration_tests.test_health import test_db_conn


def require_db_conn(func:Callable[...,Awaitable[Any]]):
    @wraps(func)
    async def wrapper(*args,**kwargs):
        
        connection = await test_db_conn()
        if not connection:
            raise HTTPException(status_code=503, detail="Database not available")
        print ("Database is ok")
    
        res = await func(*args,**kwargs)
        return res 
    return wrapper
