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

def validate_auth_user():
    pass

def randomword(length): 
   letters = string.ascii_lowercase+string.digits
   return ''.join(random.choice(letters) for i in range(length))

#получение количества рецептов:
def count_recipes(id_user,db:Session=Depends(get_db)):
    recipes_count=db.query(models.Recipe).filter(models.Recipe.id_user==id_user).filter(models.Recipe.published==True).all()
    count = recipes_count.__len__()
    return count

#функция подсчёта лайков
def likes_recipes(id_user,db:Session=Depends(get_db)):
    recipes=db.query(models.Recipe).filter(models.Recipe.id_user==id_user).all()
    likes = 0
    for recipe in recipes:
        users_likes_db=db.query(models.Score).filter(models.Score.id_recipe==recipe.id).filter(models.Score.like==True).all()
        likes = likes + users_likes_db.__len__()
    return likes

#функция подсчёта дизлайков
def dizlikes_recipes(id_user,db:Session=Depends(get_db)):
    recipes=db.query(models.Recipe).filter(models.Recipe.id_user==id_user).all()
    dizlikes = 0
    for recipe in recipes:
        users_dizlikes_db=db.query(models.Score).filter(models.Score.id_recipe==recipe.id).filter(models.Score.dizlike==True).all()
        dizlikes = dizlikes + users_dizlikes_db.__len__()
    return dizlikes

#добавление рейтинга и количества
def raiting_recipes(user_db,db:Session=Depends(get_db)):
    user_db.raiting= likes_recipes(user_db.id,db) * 2 - dizlikes_recipes(user_db.id,db)
    if user_db.raiting < 0:
        user_db.raiting=0
    user_db.count_r=count_recipes(user_db.id,db)
    return user_db

#получение пользователя
def get_current_auth_user(payload:dict=Depends(auth_utils.auth_wrapper), db:Session=Depends(get_db)):
    username:str | None = payload.get("sub")
    users_db=db.query(models.User).filter(models.User.name==username).first()
    if users_db: #вытаскиваем пользователя из бд
        raiting_recipes(users_db,db)
        return users_db
    raise HTTPException(status_code=401, detail="Токен не найден")

#получение списка пользователей
@router.get('/', response_model=List[pyd.UserScheme])
async def get_users(db:Session=Depends(get_db)):
    users=db.query(models.User).all()
    for user in users:
        raiting_recipes(user,db)
    return users

#получение топ-3 пользователей по рейтингу
@router.get('/top', response_model=List[pyd.UserScheme])
async def get_users_top(db:Session=Depends(get_db)):
    users=db.query(models.User).all()
    for user in users:
        raiting_recipes(user,db)
    sorted_users = sorted(users, key=lambda x: x.raiting, reverse=True)
    return sorted_users[0],sorted_users[1],sorted_users[2]

#добавление пользователя (регистрация)
@router.post('/reg', response_model=pyd.UserScheme)
async def reg_user(user_input:pyd.UserCreate, db: Session = Depends(get_db)):
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
    db.add(user_db)
    db.commit()
    email_verify_token=randomword(25)
    email_verify_token+=str(user_db.id)
    user_db.email_verify_code=email_verify_token
    db.commit()
    #send_email_message(user_db.mail,'Проверочное письмо для едыыыы',
    #                   f'<h1>Время кушать</h1><a href="http://127.0.0.1:8000/user/verify/?code={email_verify_token}">Время найти еду</a>')
    raiting_recipes(user_db,db)
    return user_db

#редактирование фото пользователя
@router.put('/my_profile_img', response_model=pyd.UserEditingImg)
async def update_users_img(url:str= Depends(upload_file.save_file),user:pyd.UserBase=Depends(get_current_auth_user), db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    user_db=db.query(models.User).filter(models.User.name==user.name).first()
    user_db.img_avatar=url
    db.commit()
    raiting_recipes(user_db,db)
    return user_db

#редактирование почты пользователя
@router.put('/my_profile_mail', response_model=pyd.UserEditingMail)
async def update_users_mail(user_input:pyd.UserEditingMail,user:pyd.UserBase=Depends(get_current_auth_user), db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    user_db=db.query(models.User).filter(models.User.name==user.name).first()
    user_db_0=db.query(models.User).filter(models.User.mail==user_input.mail).first() #ввёл почту
    user_db_1=db.query(models.User).where(models.User.mail==user.mail).first() #почта в дб равна почте пользователя, что сейчас зарегистрировался
    if user_db_0:
        if user_db.mail == user_input.mail:
            raise HTTPException(400, 'Ваша почта осталась вашей почтой!')
        if user_db_0.mail and user_db_0.mail != user_db_1.mail:
            raise HTTPException(400, 'Email занят')
    user_db.mail=user_input.mail
    db.commit()
    email_verify_token=randomword(25)
    email_verify_token+=str(user_db.id)
    user_db.email_verify_code=email_verify_token
    db.commit()
    send_email_message(user_db.mail,'Проверочное письмо для едыыыы',
                    f'<h1>Время кушать</h1><a href="http://127.0.0.1:8000/user/verify/?code={email_verify_token}">Время найти еду</a>')
    raiting_recipes(user_db,db)
    return user_db

#редактирование пароля пользователя
@router.put('/my_profile_pass', response_model=pyd.UserEditingPass)
async def update_users_pass(user_input:pyd.UserEditingPass,user:pyd.UserBase=Depends(get_current_auth_user), db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    user_db=db.query(models.User).filter(models.User.name==user.name).first()
    user_db.password = auth_utils.get_password_hash(user_input.password)
    db.commit()
    raiting_recipes(user_db,db)
    return user_db

#редактирование рассылки пользователя
@router.put('/my_profile_maling', response_model=pyd.UserEditingMailing)
async def update_users_maling(user_input:pyd.UserEditingMailing,user:pyd.UserBase=Depends(get_current_auth_user), db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    user_db=db.query(models.User).filter(models.User.name==user.name).first()
    user_db.mailing=user_input.mailing
    db.commit()
    raiting_recipes(user_db,db)
    return user_db

#удаление пользователя
@router.delete('/my_profile_delete')
async def delete_users(db:Session=Depends(get_db),user:pyd.UserBase=Depends(get_current_auth_user),payload:dict=Depends(auth_utils.auth_wrapper)):
    user_db=db.query(models.User).filter(models.User.name==user.name).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")
    db.delete(user_db)
    recipe_db=db.query(models.Recipe).filter(models.Recipe.id_user==user_db.id).all()
    for recipe in recipe_db:
        #удаление рецепта
        db.query(models.Recipe).filter(models.Recipe.id==recipe.id).delete()
        #удаление шагов
        db.query(models.Step).filter(models.Step.id_recipe==recipe.id).delete()
        #удаление дополнительных фото
        db.query(models.Additional_photo).filter(models.Additional_photo.id_recipe==recipe.id).delete()
        #удаление количества
        db.query(models.Count).filter(models.Count.id_recipe==recipe.id).delete()
        #удаление оценок
        db.query(models.Score).filter(models.Score.id_recipe==recipe.id).delete()
    db.query(models.Score).filter(models.Score.id_user==user_db.id).delete()
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

#вход пользователя
@router.post("/login", response_model=TokenInfo)
def auth_user_issue_jwt(cred: pyd.Credentials, db:Session=Depends(get_db)):
    cred_db=db.query(models.User).filter(models.User.mail==cred.mail).first()
    if not cred_db:
        raise HTTPException(404, 'Пользователь не найден!')
    if not auth_utils.verify_password(cred.pwd, cred_db.password):
        raise HTTPException(404, 'Неверный логин или пароль')
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

#проверка токена
@router.get("/me")
def auth_user_check_self_info(payload:dict=Depends(auth_utils.auth_wrapper), user:pyd.UserScheme=Depends(get_current_auth_user)):
    return {
        "username": user.name,
        "email": user.mail,
        "count_r": user.count_r,
        "raiting": user.raiting,
        "mailing":user.mailing
        }



    