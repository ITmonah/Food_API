import jwt
from config import settings
from datetime import timedelta, datetime
from passlib.context import CryptContext
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

#private_key = b"-----BEGIN PRIVATE KEY-----\nMIGEAgEAMBAGByqGSM49AgEGBS..."
#public_key = b"-----BEGIN PUBLIC KEY-----\nMHYwEAYHKoZIzj0CAQYFK4EEAC..."


#настройки для хеширования пароля
security = HTTPBearer()
pwd_context = CryptContext(
    schemes=['bcrypt'],
    deprecated='auto'
)

#функция получения хеша из пароля
def get_password_hash(password):
    return pwd_context.hash(password)

#сверка пароля и хеша
def verify_password(input_pass, hash_pass):
    return pwd_context.verify(input_pass, hash_pass)

#создание JWT токена
def encode_jwt(
        payload:dict,
        private_key:str = settings.auth_jwt.private_key_path.read_text(),
        algorithm:str = settings.auth_jwt.algrotihm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes
        #expire_timedelta: timedelta | None = None, #можно самим задавать время жизни токена
):
    #пишем отдельно, чтобы не менять чужой словарь
    to_encode = payload.copy()
    now = datetime.utcnow()
    #if expire_timedelta:
    #    expire = now + expire_timedelta
    #else: 
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        #служебные поля
        exp=expire,
        iat=now
        )
    encoded = jwt.encode(
        payload,
        private_key,
        algorithm=algorithm
    )
    return encoded

def decode_jwt(
        token:str | bytes,
        public_key:str = settings.auth_jwt.public_key_path.read_text(),
        algorithm:str = settings.auth_jwt.algrotihm
):
    try:
        decoded = jwt.decode(
            token,
            public_key,
            algorithms=[algorithm]
            )
        return decoded
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, 'Просрочено')
    except jwt.InvalidTokenError as e:
        raise HTTPException(401, 'Плохой токен')

# мидлваре для защиты маршрутов
def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(security)):
    token = auth.credentials
    try:
        payload = decode_jwt(token=token)
    except jwt.InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Токен неверен!: {e}")
    return payload
    #return decode_jwt(auth.credentials)
