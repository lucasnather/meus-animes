import jwt
from datetime import timedelta, datetime

class Jwt:

    def __init__(self) -> None:
        self.secret_key = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
        self.algorithm = "HS256"
        self.access_token_expire_minutes = 30

    def generate_token(self, data: dict):
        to_encode = data.copy()
        expire =  datetime.utcnow() + timedelta(seconds=900)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm], options={"verify_exp": True})
            return payload
        except jwt.ExpiredSignatureError:
            print("Token expirado")
            return None
        except jwt.InvalidTokenError as e:
            print(f"Token inválido: {str(e)}")
            return None
        