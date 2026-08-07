import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import jwt


# Отвественен за простые операции типо создания/удаления/хэширования паролей, токенов и подобной мути, помогатор проще говоря
class TokenHelper:
    
    def generate_sesion_token(self) -> tuple[str,str]:
        """Создает пару значений (сырой токен, хэш)"""
        token = secrets.token_urlsafe(32)
        return token,self.hash_session_token(token)
    
    def hash_session_token(self,token:str):
        """Хэширует токен c помощью SHA-256"""
        return hashlib.sha256(token.encode("utf-8")).hexdigest()
    
    def create_access_token(self,user_id:int):
        """Формирует JWT access c типом access и истечением из настроек"""
        return self._create_token(user_id,"access",)
    
    def create_refresh_token(self) -> str:
        return secrets.token_urlsafe(50)
        
    def decode_token(self) -> dict:
        payload = jwt.decode() #токен, ключ, алгоритм шифрования
        return payload
    
    def _create_token(self,user_id:int, token_type:str,expires_minutes:int) -> str:
        """Собирает JWT c указанным типом и временем жизни"""
        now = datetime.now(timezone.utc)
        payload = {
            "sub":str(user_id),
            "type":token_type,
            "iat":int(now.timestamp()),
            "exp":int((now + timedelta(minutes=expires_minutes)).timestamp()),
            "iss":"Auth"
        }
        return jwt.encode(payload)