import hashlib
import bcrypt


class Security:
    
    def hash_password(self,password:str) -> str:
        """прокидываем прэхеш и заканчиваем хэширование на толстой ноте"""
        digest = self._password_digest(password=password)
        return bcrypt.hashpw(digest,bcrypt.gensalt()).decode("utf-8")
    
    def verify_password(self,password:str,password_hash:str):
        digest = self._password_digest(password=password)
        return bcrypt.checkpw(digest,hashed_password=password_hash.encode("utf-8"))
    
    def _password_digest(self,password:str) -> bytes:
        """Ебашим прехэш, дабы обойти проблему 72 байт в bcrypt(SHA256 выдает где-то 32-64 байта)"""
        return hashlib.sha256(password.encode("utf-8")).digest()
        