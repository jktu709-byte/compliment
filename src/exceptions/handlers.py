# ХЭНДЛЕР НУЖЕН ДЛЯ ПРАВИЛЬНОГО СООТНОШЕНИЯ СЕМАНТИЧЕСКИХ, ТЕХНИЧЕСКИХ ОЩИБОК И ВОЗВРАЩЕНИЯ ВЕРНОГО ОТВЕТА ПОЛЬЗОВАТЕЛЮ И РАЗРАБУ
from collections.abc import Callable, Coroutine #noqa
from functools import wraps

# чтож начало положено. ну я и лох конечно
class ExceptionHandler:
    
    def __init__(self) -> None:
        pass
    
    # отлов базовых ошибок
    def app_error_handler(self,func:Callable): # type: ignore
        @wraps(func)
        def wrapper():
             res = func()
             return res
        return wrapper
    
    def validation_error_handler(self,func):
        @wraps(func)
        def wrapper():
            res = func()
            return res
        return wrapper
    
    