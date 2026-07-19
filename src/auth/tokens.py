import hashlib
import secrets
from datetime import datetime,timezone,timedelta
import jwt

class TokenHelper:
    
    def generate_sesion_token(self) -> tuple[str,str]:
        """Создает пару значений (сырой токен, хэш)"""
        token = secrets.token_urlsafe(32)
        return token,self.hash_session_token(token)
    
    def hash_session_token(self,token:str):
        """Хэширует токен с помощью SHA-256"""
        return hashlib.sha256(token.encode("utf-8")).hexdigest()
    
    def create_access_token(self,user_id:int):
        """"""
        return self._create_token(user_id,"access",)
    def _create_token(self,user_id:int, token_type:str,expires_minutes:int) -> str:
        now = datetime.now(timezone.utc)
        payload = {
            "sub":str(user_id),
            "type":token_type,
            "iat":int(now.timestamp()),
            "exp":int((now + timedelta(minutes=expires_minutes)).timestamp()),
            "iss":...
        }
        return jwt.encode(payload)