import jwt
from config import settings
from datetime import timedelta, datetime

#private_key = b"-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBS..."
#public_key = b"-----BEGIN PUBLIC KEY-----\nMHYwEAYHKoZIzj0CAQYFK4EEAC..."

def encode_jwt(
        payload:dict,
        private_key:str = settings.auth_jwt.private_key_path.read_text(),
        algorithm:str = settings.auth_jwt.algrotihm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None, #можно самим задавать время жизни токена
):
    #пишем отдельно, чтобы не менять чужой словарь
    to_encode = payload.copy()
    now = datetime.utcnow()
    if expire_timedelta:
        expire = now + expire_timedelta
    else: 
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        #служебные поля
        exp=expire,
        iat=now,
        )
    encoded = jwt.encode(
        payload,
        private_key,
        algorithm=algorithm,
    )
    return encoded

def decode_jwt(
        token:str | bytes,
        public_key:str = settings.auth_jwt.public_key_path.read_text(),
        algorithm:str = settings.auth_jwt.algrotihm,
):
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
        )
    return decoded
