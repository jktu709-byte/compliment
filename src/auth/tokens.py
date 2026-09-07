import hashlib
import secrets
from datetime import datetime, timedelta, timezone

from jwt import JWT


# Отвественен за простые операции типо создания/удаления/хэширования паролей, токенов и подобной мути, помогатор проще говоря
class TokenHelper:
    def __init__(self) -> None:
        self.token_jwt = JWT()
    
    def generate_sesion_token(self) -> tuple[str,str]:
        """Создает пару значений (сырой токен, хэш)"""
        token = secrets.token_urlsafe(32)
        return token,self.hash_session_token(token)
    
    def hash_session_token(self,token:str):
        """Хэширует токен c помощью SHA-256"""
        return hashlib.sha256(token.encode("utf-8")).hexdigest()
    
    def create_access_token(self,user_id:int):
        """Формирует JWT access c типом access и истечением из настроек"""
        return self._create_token(user_id,"access",15)
    
    def create_refresh_token(self) -> str:
        return secrets.token_urlsafe(50)
        
    def decode_token(self) -> dict:
        payload = self.token_jwt.decode() # type: ignore #токен, ключ, алгоритм шифрования
        return payload
    
    def _create_token(self,user_id:int, token_type:str,expires_minutes:int) -> str:
        """Собирает JWT c указанным типом и временем жизни"""
        now = datetime.now(timezone.utc)
        expires = now + timedelta(minutes=expires_minutes)

        payload = {
            "sub": str(user_id),
            "type": token_type,
            "iat": int(now.timestamp()),
            "exp": int(expires.timestamp()),
            "iss": "Auth",
        }
                
        return self.token_jwt.encode(payload=payload)
# Если не сделать экземпляр класса, тогда везде будет требоваться навязчивый self и портить жизнь
token_helper = TokenHelper()
