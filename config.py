from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import EmailStr, BaseModel
from pathlib import Path

BASE_DIR= Path(__file__).parent

#указание путей к ключам
class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "certs" / "jwt-public.pem"
    algrotihm: str = "RS256" #специальный алгоритм, который используется при наличии двух ключей
    access_token_expire_minutes: int = 3 #минуты

class TokenInfo(BaseModel):
    access_token:str
    token_type:str

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./sql_app.sqlite"

    EMAIL_SMTP:str
    EMAIL_PORT:str='465'
    EMAIL_LOG:str
    EMAIL_PWD:str

    model_config = SettingsConfigDict(env_file=".env")

    auth_jwt:AuthJWT = AuthJWT()

settings = Settings()

