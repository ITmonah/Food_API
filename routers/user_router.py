from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from database import get_db
import pyd
import random, string
from myemail import send_email_message
#модули для связи бэка с фронтом
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

def randomword(length): 
   letters = string.ascii_lowercase+string.digits
   return ''.join(random.choice(letters) for i in range(length))

#получение списка пользователей
@router.get('/', response_model=List[pyd.UserBase])
async def get_users(db:Session=Depends(get_db)):
    users=db.query(models.User).all()
    return users

#добавление пользователя (регистрация)
@router.post('/',response_model=pyd.UserBase)
async def reg_user(user_input:pyd.UserCreate,db: Session = Depends(get_db)):
    user_db=db.query(models.User).filter(models.User.mail==user_input.mail).first()
    user_db_2=db.query(models.User).filter(models.User.name==user_input.name).first()
    if user_db:
        raise HTTPException(400, 'Email занят')
    if user_db_2:
        raise HTTPException(400, 'Никнейм занят')
    user_db=models.User()
    user_db.name=user_input.name
    user_db.mail=user_input.mail
    user_db.password=user_input.password
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
async def update_users(user_id:int, user_input:pyd.UserCreate, db:Session=Depends(get_db)):
    user_db=db.query(models.User).filter(models.User.id==user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")
    user_db.name=user_input.name
    user_db.mail=user_input.mail
    user_db.password=user_input.password
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
async def delete_users(user_id:int, db:Session=Depends(get_db)):
    user_db=db.query(models.User).filter(models.User.id==user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")
    db.delete(user_db)
    #удаление рецепта
    db.query(models.Recipe).filter(models.Recipe.id_user==user_id).delete()
    db.commit()
    return "Удаление пользователя прошло успешно!"

@router.get('/verify')
async def verify_email(code:str,db: Session = Depends(get_db)):
    user_db=db.query(models.User).filter(models.User.email_verify_code==code).first()
    if not user_db:
        raise HTTPException(400, 'Неверный код')
    user_db.email_verify=True
    user_db.email_verify_code=None
    db.commit()
    return RedirectResponse('http://127.0.0.1:8000')