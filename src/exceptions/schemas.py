from pydantic import BaseModel


# Эта штука указывает на конкретное место(проблемное поле), что упрощает поиск ошибок
class ErrorDetail(BaseModel):
    # Само поле
    field:str
    # Что конкретно не так
    msg:str
       
class ErrorResponse(BaseModel):
    # Статус
    code:str
    # Сообщение
    msg:str
    # Если надо, может вернуть и конкретные ответы(у меня их все равно нет)
    details:list[ErrorDetail]

