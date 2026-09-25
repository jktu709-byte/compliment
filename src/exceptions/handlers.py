# ХЭНДЛЕР НУЖЕН ДЛЯ ПРАВИЛЬНОГО СООТНОШЕНИЯ СЕМАНТИЧЕСКИХ, ТЕХНИЧЕСКИХ ОЩИБОК И ВОЗВРАЩЕНИЯ ВЕРНОГО ОТВЕТА ПОЛЬЗОВАТЕЛЮ И РАЗРАБУ
from functools import wraps #noqa

from fastapi import Request
from fastapi.responses import JSONResponse

from src.exceptions.semantic_exceptions import AppError, ComplimentAlreadyExistsError, ComplimentNotFoundError, InvalidCredentialsError, RefreshTokenExpiredError, RefreshTokenNotFoundError, UserAlreadyExistsError, UserNotFoundError
# мапа для соотношения разных ошибок и статус кодов
ERROR_STATUS_CODES = {
    UserNotFoundError: 404,
    UserAlreadyExistsError: 409,
    InvalidCredentialsError: 401,
    RefreshTokenNotFoundError: 404,
    RefreshTokenExpiredError: 401,
    ComplimentAlreadyExistsError: 409,
    ComplimentNotFoundError: 404,
}

async def app_error_hadler(req:Request,exc:AppError) -> JSONResponse:
    status_code = ERROR_STATUS_CODES.get(type(exc),400)
    return JSONResponse(
        status_code=status_code,
        content={"code":exc.code,"msg":exc.msg}
    )

# идею с классом реализую возможно позже
# class ExceptionHandler:
    
#     def __init__(self) -> None:
#         pass
    

    
    