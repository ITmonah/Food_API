from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from database import get_db
import pyd
#модули для JWT токена
import auth_utils
from config import TokenInfo

router = APIRouter(
    prefix="/mealtime",
    tags=["mealtime"],
)

#получение списка время приёма пищи
@router.get('/', response_model=List[pyd.MealtimeBase])
async def get_mealtimes(db:Session=Depends(get_db)):
    mealtimes=db.query(models.Mealtime).all()
    return mealtimes

#добавление времени приёма пищи
@router.post('/', response_model=pyd.MealtimeBase)
async def create_mealtimes(mealtime_input:pyd.MealtimeCreate, db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    mealtime_db=models.Mealtime()
    mealtime_db.name=mealtime_input.name
    db.add(mealtime_db)
    db.commit()
    return mealtime_db

#редактирование времени приёма пищи
@router.put('/{mealtime_id}', response_model=pyd.CategoryBase)
async def update_mealtimes(mealtime_id:int, mealtime_input:pyd.CategoryBase, db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    mealtime_db=db.query(models.Mealtime).filter(models.Mealtime.id==mealtime_id).first()
    if not mealtime_db:
        raise HTTPException(status_code=404, detail="Время приёма пищи не найдено!")
    mealtime_db.name=mealtime_input.name
    db.commit()
    return mealtime_db

#удаление времени приёма пищи
@router.delete('/{mealtime_id}')
async def delete_mealtimes(mealtime_id:int, db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    mealtime_db=db.query(models.Mealtime).filter(models.Mealtime.id==mealtime_id).first()
    if not mealtime_db:
        raise HTTPException(status_code=404, detail="Время приёма пищи не найдено!")
    db.delete(mealtime_db)
    db.commit()
    return "Удаление времени приёма пищи прошло успешно!"
