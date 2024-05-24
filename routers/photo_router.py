from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from typing import List
import models
from database import get_db
import pyd
import upload_file
#модули для JWT токена
import auth_utils
from config import TokenInfo

router = APIRouter(
    prefix="/photo",
    tags=["photo"],
)

#получение ссылок на фото
@router.get('/', response_model=List[pyd.Additional_photoScheme])
async def get_photos(db:Session=Depends(get_db)):
    photo=db.query(models.Additional_photo).all()
    return photo

#добавление фото
@router.post('/')
async def create_photos(files:list[UploadFile],db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.name==payload.get("username")).first() #получаем пользователя
    recipe_db = db.query(models.Recipe).filter(models.Recipe.id_user==user_db.id).order_by(models.Recipe.created_at.desc()).first() #находим рецепт, принадлежащий пользователю
    for img in files:
        photo_db=models.Additional_photo()
        photo_db.img=upload_file.save_file(img)
        photo_db.id_recipe=recipe_db.id
        db.add(photo_db)
        db.commit()
    return "Фото добавлены успешно"

#редактирование фото
@router.put('/{photo_id}', response_model=pyd.Additional_photoScheme)
async def update_photos(photo_id:int, url:str= Depends(upload_file.save_file),photo_input:pyd.Additional_photoCreate=Depends(), db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    photo_db=db.query(models.Additional_photo).filter(models.Additional_photo.id==photo_id).first()
    if not photo_db:
        raise HTTPException(status_code=404, detail="Фото не найдено!")
    photo_db.img=url
    photo_db.id_recipe=photo_input.id_recipe
    db.add(photo_db)
    db.commit()
    return photo_db

#удаление фото
@router.delete('/{photo_id}')
async def delete_ingredients(photo_id:int, db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    photo_db=db.query(models.Additional_photo).filter(models.Additional_photo.id==photo_id).first()
    if not photo_db:
        raise HTTPException(status_code=404, detail="Фото не найдено!")
    db.delete(photo_db)
    db.commit()
    return "Удаление фото прошло успешно!"