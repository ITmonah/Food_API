from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import models
from database import get_db
import pyd
import random, string
from myemail import send_email_message
import upload_file
import shutil
#модули для связи бэка с фронтом
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
#модули для хэширования пароля
import os, hashlib
#модули для JWT токена
import auth_utils
from config import TokenInfo
#модули для получения Bearer токена из заголовков
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials, OAuth2PasswordBearer 
#модуль для указания ошибки токена
from jwt.exceptions import InvalidTokenError

router = APIRouter(
    prefix="/user",
    tags=["user"],
)
http_bearer = HTTPBearer() #получаем токен из запроса
#oauth2_sheme = OAuth2PasswordBearer(tokenUrl="/user/login") #откуда пришёл токен

def randomword(length): 
   letters = string.ascii_lowercase+string.digits
   return ''.join(random.choice(letters) for i in range(length))

#получение списка пользователей
@router.get('/', response_model=List[pyd.UserBase])
async def get_users(db:Session=Depends(get_db)):
    users=db.query(models.User).all()
    return users

#добавление пользователя (регистрация)
@router.post('/reg', response_model=pyd.UserBase)
async def reg_user(url:str= Depends(upload_file.save_file),user_input:pyd.UserCreate=Depends(), db: Session = Depends(get_db)):
    user_db=db.query(models.User).filter(models.User.mail==user_input.mail).first()
    user_db_2=db.query(models.User).filter(models.User.name==user_input.name).first()
    if user_db:
        raise HTTPException(400, 'Email занят')
    if user_db_2:
        raise HTTPException(400, 'Никнейм занят')
    user_db=models.User()
    user_db.name=user_input.name
    user_db.mail=user_input.mail
    user_db.password = auth_utils.get_password_hash(user_input.password)
    user_db.img_avatar=url
    user_db.mailing=user_input.mailing
    db.add(user_db)
    db.commit()
    email_verify_token=randomword(25)
    email_verify_token+=str(user_db.id)
    user_db.email_verify_code=email_verify_token
    db.commit()
    send_email_message(user_db.mail,'Проверочное письмо для едыыыы',
                       f'<h1>Время кушать</h1><a href="http://127.0.0.1:8000/user/verify/?code={email_verify_token}">Время найти еду</a>')
    return user_db

#редактирование пользователя
@router.put('/{user_id}', response_model=pyd.UserBase)
async def update_users(user_id:int, url:str= Depends(upload_file.save_file),user_input:pyd.UserCreate=Depends(), db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    user_db=db.query(models.User).filter(models.User.id==user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")
    user_db_1=db.query(models.User).filter(models.User.mail==user_input.mail).first()
    user_db_2=db.query(models.User).filter(models.User.name==user_input.name).first()
    if user_db_1:
        raise HTTPException(400, 'Email занят')
    if user_db_2:
        raise HTTPException(400, 'Никнейм занят')
    user_db.name=user_input.name
    user_db.mail=user_input.mail
    user_db.password = auth_utils.get_password_hash(user_input.password)
    user_db.img_avatar=url
    user_db.mailing=user_input.mailing
    db.commit()
    email_verify_token=randomword(25)
    email_verify_token+=str(user_db.id)
    user_db.email_verify_code=email_verify_token
    db.commit()
    send_email_message(user_db.mail,'Проверочное письмо для едыыыы',
                       f'<h1>Время кушать</h1><a href="http://127.0.0.1:8000/user/verify/?code={email_verify_token}">Время найти еду</a>')
    return user_db

#удаление пользователя
@router.delete('/{user_id}')
async def delete_users(user_id:int, db:Session=Depends(get_db),user=Depends(auth_utils.auth_wrapper),payload:dict=Depends(auth_utils.auth_wrapper)):
    user_db=db.query(models.User).filter(models.User.id==user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")
    db.delete(user_db)
    #удаление рецепта
    db.query(models.Recipe).filter(models.Recipe.id_user==user_id).delete()
    db.commit()
    return "Удаление пользователя прошло успешно!"

#верификация пользователя
@router.get('/verify')
async def verify_email(code:str,db: Session = Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    user_db=db.query(models.User).filter(models.User.email_verify_code==code).first()
    if not user_db:
        raise HTTPException(400, 'Неверный код')
    user_db.email_verify=True
    user_db.email_verify_code=None
    db.commit()
    return RedirectResponse('http://127.0.0.1:8000')

def validate_auth_user():
    pass

#вход пользователя
@router.post("/login", response_model=TokenInfo)
def auth_user_issue_jwt(cred: pyd.Credentials, db:Session=Depends(get_db)):
    cred_db=db.query(models.User).filter(models.User.mail==cred.mail).first()
    if not cred_db:
        raise HTTPException(404, 'Пользователь не найден!')
    if not auth_utils.verify_password(cred.pwd, cred_db.password):
        raise HTTPException(403, 'Не верный логин или пароль')
    jwt_payload = {
        #кому это принадлежит
        "sub": cred_db.name,
        "username": cred_db.name,
        "email": cred.mail,
    }
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type="Bearer", #стандартный тип токена
    )

#получение paylaod токена
"""def get_current_token_payload(
        credentials:HTTPAuthorizationCredentials=Depends(http_bearer)
        #token:str=Depends(oauth2_sheme)
        ):
    token = credentials.credentials
    try:
        payload = auth_utils.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Токен неверен!: {e}")
    return payload"""

#получение пользователя
def get_current_auth_user(payload:dict=Depends(auth_utils.auth_wrapper), db:Session=Depends(get_db)):
    username:str | None = payload.get("sub")
    users_db=db.query(models.User).filter(models.User.name==username).first()
    if users_db: #вытаскиваем пользователя из бд
        return users_db
    raise HTTPException(status_code=401, detail="Токен не найден")

#проверка пользователя на активность
#def get_current_active_auth_user(user:pyd.UserBase=Depends(get_current_auth_user)):
#    if user.active:
#        return user
#    raise HTTPException(status_code=403, detail="Пользователь не активен")

#проверка токена
@router.get("/me")
def auth_user_check_self_info(payload:dict=Depends(auth_utils.auth_wrapper), user:pyd.UserBase=Depends(get_current_auth_user)):
    iat = payload.get("iat")
    return {
        "username": user.name,
        "email": user.mail,
        "logged_in_ait": iat
        }
    