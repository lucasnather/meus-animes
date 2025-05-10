from passlib.hash import bcrypt

class PasswordHash:
    
    def hash_password(self, password: str) -> str:
        return bcrypt.hash(password)
    
    def verify_password(self, password: str, db_password) -> bool:
        return bcrypt.verify(password, db_password)
