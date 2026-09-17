# ХЭНДЛЕР НУЖЕН ДЛЯ ПРАВИЛЬНОГО СООТНОШЕНИЯ СЕМАНТИЧЕСКИХ, ТЕХНИЧЕСКИХ ОЩИБОК И ВОЗВРАЩЕНИЯ ВЕРНОГО ОТВЕТА ПОЛЬЗОВАТЕЛЮ И РАЗРАБУ
from functools import wraps

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.exceptions.semantic_exceptions import AppError


# чтож начало положено. ну я и лох конечно
class ExceptionHandler:
    
    def __init__(self) -> None:
        pass
    
    # отлов базовых ошибок
    @staticmethod
    async def app_error_handler(request: Request,exc: AppError,) -> JSONResponse: ... # type: ignore
        # @wraps(func)
        # def wrapper():
        #      res = func()
        #      return res
        # return wrapper
    
    @staticmethod
    async def validation_error_handler(request: Request,exc: RequestValidationError) -> JSONResponse: ...
        # @wraps(func)
        # def wrapper():
        #     res = func()
        #     return res
        # return wrapper
    
    