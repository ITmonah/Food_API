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
    prefix="/step",
    tags=["step"],
)

#получение списка шагов
@router.get('/', response_model=List[pyd.StepScheme])
async def get_steps(db:Session=Depends(get_db)):
    steps=db.query(models.Step).all()
    return steps

#добавление шага
@router.post('/', response_model=pyd.StepScheme)
async def create_steps(step_input:List[pyd.StepCreate], db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.name==payload.get("username")).first() #получаем пользователя
    recipe_db = db.query(models.Recipe).filter(models.Recipe.id_user==user_db.id).order_by(models.Recipe.created_at.desc()).first() #находим рецепт, принадлежащий пользователю
    for step in step_input:
        step_db=models.Step()
        step_db.number=(step_input.index(step)) + 1
        step_db.info=step.info
        step_db.recipe=recipe_db
        db.add(step_db)
        db.commit()
    return step_db

#редактирование шага
@router.put('/{step_id}', response_model=pyd.StepScheme)
async def update_steps(step_id:int, step_input:pyd.StepCreate, db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    step_db=db.query(models.Step).filter(models.Step.id==step_id).first()
    if not step_db:
        raise HTTPException(status_code=404, detail="Шаг не найден!")
    step_db.number=step_input.number
    step_db.info=step_input.info
    #рецепт - один
    recipe_db = db.query(models.Recipe).filter(models.Recipe.id==step_input.id_recipe).first()
    if not recipe_db:
        raise HTTPException(status_code=404, detail="Рецепт не найден!")
    step_db.recipe=recipe_db #отношение
    db.commit()
    return step_db

#удаление шага
@router.delete('/{step_id}')
async def delete_steps(step_id:int, db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    step_db=db.query(models.Step).filter(models.Step.id==step_id).first()
    if not step_db:
        raise HTTPException(status_code=404, detail="Шаг не найден!")
    db.delete(step_db)
    db.commit()
    return "Удаление шага прошло успешно!"