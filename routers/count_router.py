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
    prefix="/count",
    tags=["count"],
)

#получение списка количества
@router.get('/', response_model=List[pyd.CountScheme])
async def get_counts(db:Session=Depends(get_db)):
    count_db=db.query(models.Count).all()
    return count_db

#добавление количества ингредиентов
@router.post('/', response_model=pyd.CountScheme)
async def create_counts(count_input:List[pyd.CountCreate], db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.name==payload.get("username")).first() #получаем пользователя
    recipe_db = db.query(models.Recipe).filter(models.Recipe.id_user==user_db.id).order_by(models.Recipe.created_at.desc()).first() #находим рецепт, принадлежащий пользователю
    for count_int in count_input:
        count_db=models.Count()
        count_db.recipe=recipe_db #добавляю рецепт
        ing_db=db.query(models.Ingredient).filter(models.Ingredient.id==count_int.id_ingredient).first() #получаем пользователя
        if not ing_db:
            raise HTTPException(status_code=404, detail="Ингредиент не найден!")
        count_db.id_ingredient=ing_db.id
        count_db.count=count_int.count
        sys_db=db.query(models.System_of_calculation).filter(models.System_of_calculation.id==count_int.id_system_of_calc).first() #получаем пользователя
        if not sys_db:
            raise HTTPException(status_code=404, detail="Система исчисления не найдена!")
        count_db.id_system_of_calc = sys_db.id
        db.add(count_db)
        db.commit()
    return count_db
