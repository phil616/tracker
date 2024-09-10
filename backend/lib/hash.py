import hashlib
import bcrypt

class Hash:

    def bcrypt(self, password: str) -> str:
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_bcrypt(self, password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
    
    def sha256(self, data: str) -> str:
        return hashlib.sha256(data.encode('utf-8')).hexdigest()
    
    def sha512(self, data: str) -> str:
        return hashlib.sha512(data.encode('utf-8')).hexdigest()
    
    def md5(self, data: str) -> str:
        return hashlib.md5(data.encode('utf-8')).hexdigest()
    
    def byte_hash(self, data: bytes) -> str:
        return hashlib.sha256(data).hexdigest()

hash_util = Hash()
