from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException, Request
from dotenv import load_dotenv
from typing import Union, Any
import os

load_dotenv()

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7
secret_key = os.getenv("JWT_SECRET_KEY")
refresh_key = os.getenv("JWT_REFRESH_KEY")

hass_password = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash_password(password: str) -> str:
    return hass_password.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return hass_password.verify(plain_password, hashed_password)


def create_access_token(user_id: int, subject: Union[str, Any], expires_delta: int = None, ) -> str:
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    encode = {'user_id': user_id, 'exp': expires_delta, 'sub': str(subject)}
    encode_jwt = jwt.encode(encode, secret_key, algorithm=ALGORITHM)

    return encode_jwt


def refresh_token(subject: Union[str, Any], expire_delta: int = None) -> str:
    if expire_delta is not None:
        expire_delta = datetime.utcnow() + expire_delta
    else:
        expire_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    encode = {'exp': expire_delta, 'sub': str(subject)}
    encode_jwt = jwt.encode(encode, refresh_key, algorithm=ALGORITHM)

    return encode_jwt


def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(status_code=403, detail="Invalid token")


class JWT_Bearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWT_Bearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWT_Bearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            payload = decode_jwt(jwtoken)
            if payload and "exp" in payload:
                if datetime.utcfromtimestamp(payload["exp"]) < datetime.utcnow():
                    return False
            return payload is not None
        except:
            return False


jwt_bearer = JWT_Bearer()
