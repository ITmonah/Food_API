from fastapi import APIRouter, Depends, HTTPException
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
    prefix="/recipe",
    tags=["recipe"],
)

#получение списка рецептов
@router.get('/', response_model=List[pyd.RecipeScheme])
async def get_recipes(db:Session=Depends(get_db)):
    recipes=db.query(models.Recipe).all()
    return recipes

#добавление рецепта
@router.post('/', response_model=pyd.RecipeScheme)
async def create_recipes(url:str= Depends(upload_file.save_file),recipe_input:pyd.RecipeCreate=Depends(), db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    recipe_db=models.Recipe()
    recipe_db.name=recipe_input.name
    recipe_db.face_img=url
    #категория - одна
    category_db = db.query(models.Category).filter(models.Category.id==recipe_input.id_category).first()
    if category_db:
        recipe_db.category=category_db #отношение
    else:
        raise HTTPException(status_code=404, detail="Категория не найдена!")
    #пользователь - одна
    user_db = db.query(models.User).filter(models.User.id==recipe_input.id_user).first()
    if user_db:
        recipe_db.user=user_db
    else:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")
    #время приёма пищи  - несколько 
    for id_mealtime in recipe_input.id_mealtime:
        mealtime_db = db.query(models.Mealtime).filter(models.Mealtime.id==id_mealtime).first()
        if mealtime_db:
            recipe_db.mealtime.append(mealtime_db)
        else:
            raise HTTPException(status_code=404, detail="Время приёма пищи не найдено!")
    #ингредиенты  - несколько 
    for id_ingredient in recipe_input.id_ingredient:
        ingredient_db = db.query(models.Ingredient).filter(models.Ingredient.id==id_ingredient).first()
        if ingredient_db:
            recipe_db.ingredient.append(ingredient_db)
        else:
            raise HTTPException(status_code=404, detail="Ингредиент не найден!")
    recipe_db.cooking_time=recipe_input.cooking_time
    db.add(recipe_db)
    db.commit()
    return recipe_db

#редактирование рецепта
@router.put('/{recipe_id}', response_model=pyd.RecipeScheme)
async def update_recipes(recipe_id:int, url:str= Depends(upload_file.save_file),recipe_input:pyd.RecipeCreate=Depends(), db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    recipe_db=db.query(models.Recipe).filter(models.Recipe.id==recipe_id).first()
    if not recipe_db:
        raise HTTPException(status_code=404, detail="Рецепт не найден!")
    recipe_db.name=recipe_input.name
    recipe_db.face_img=url
    #категория - одна
    category_db = db.query(models.Category).filter(models.Category.id==recipe_input.id_category).first()
    if not category_db:
        raise HTTPException(status_code=404, detail="Категория не найдена!")
    recipe_db.category=category_db
    #пользователь - одна
    user_db = db.query(models.User).filter(models.User.id==recipe_input.id_user).first()
    if not user_db:
        raise HTTPException(status_code=404, detail="Пользователь не найден!")
    recipe_db.user=user_db
    #время приёма пищи  - несколько
    for mealtime_id in recipe_input.id_mealtime:
        mealtime_db = db.query(models.Mealtime).filter(models.Mealtime.id==mealtime_id).first()
        if mealtime_db:
            recipe_db.mealtime.clear()
            recipe_db.mealtime.append(mealtime_db)
        else:
            raise HTTPException(status_code=404, detail="Время приёма пищи не найдено!")
    #ингредиенты  - несколько
    for ingredient_id in recipe_input.id_ingredient:
        ingredient_db = db.query(models.Ingredient).filter(models.Ingredient.id==ingredient_id).first()
        if ingredient_db:
            recipe_db.ingredient.clear()
            recipe_db.ingredient.append(ingredient_db)
        else:
            raise HTTPException(status_code=404, detail="Ингредиент не найден!")
    recipe_db.cooking_time=recipe_input.cooking_time
    db.commit()
    return recipe_db

#удаление рецепта
@router.delete('/{recipe_id}')
async def delete_recipes(recipe_id:int, db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    recipe_db=db.query(models.Recipe).filter(models.Recipe.id==recipe_id).first()
    if not recipe_db:
        raise HTTPException(status_code=404, detail="Рецепт не найден!")
    db.delete(recipe_db)
    #удаление шагов
    db.query(models.Step).filter(models.Step.id_recipe==recipe_id).delete()
    #удаление дополнительных фото
    db.query(models.Additional_photo).filter(models.Additional_photo.id_recipe==recipe_id).delete()
    db.commit()
    return "Удаление рецепта прошло успешно!"