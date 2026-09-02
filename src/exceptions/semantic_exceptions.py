# итак мне нужно прописать ошибки так, чтобы они стали более информативными. 
class AppError(Exception):
    """Базовая ошибка приложения."""
    code:str
    msg:str
    def __init__(self, msg):
        super().__init__(msg)
          
class InvalidCredentialsError(AppError):
    """Неверная пара логин/пароль."""
    code = "INVALID_LOGIN_OR_PASSWORD"
    msg = "Invalid login or password"

class UserAlreadyExistsError(AppError):
    """Пользователь уже существует."""
    code = "USER_ALREADY_EXISTS"
    msg ="User already exists"

class UserNotFoundError(AppError):
    """Пользователь не найден."""
    code = "USER_NOT_FOUND"
    msg = "User not found"

class RefreshTokenNotFoundError(AppError):
    """Рефреш токен не найден или отозван."""
    code = "REFRESH_TOKEN_NOT_FOUND"
    msg = "Refresh token not found"

class RefreshTokenExpiredError(AppError):
    """Истек рефреш токен"""
    code = "REFRSH_TOKEN_EXPIRED"
    msg = "Refresh token expired"
    
class ComplimentAlreadyExistsError(AppError):
    """Комплимент уже существует"""
    code = "COMPLIMENT_ALREADY_EXISTS"
    msg = "Compliment already exists"

class ComplimentNotFoundError(AppError):
    """Комплимент не был найден"""
    code = "COMPLIMENT_NOT_FOUND"
    msg = "Compliment not found"