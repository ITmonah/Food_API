from fastapi import APIRouter, Depends, HTTPException, UploadFile
from pathlib import Path
from fastapi.responses import FileResponse
#joinedload - подходит для многие к одному, один к одному
# - многие ко многим, один ко многим
from sqlalchemy import and_, text, insert, select, func, cast, or_
from sqlalchemy.orm import Session, joinedload, selectinload, contains_eager
from typing import List
import models
from database import get_db
import pyd
import upload_file
#модули для JWT токена
import auth_utils
from config import TokenInfo
#модули для пагинации
from fastapi_pagination import Page, LimitOffsetPage, paginate, add_pagination, limit_offset
from fastapi_pagination.utils import disable_installed_extensions_check

router = APIRouter(
    prefix="/recipe",
    tags=["recipe"],
)

#функция подсчёта лайков
def likes_recipes(recipe,db:Session=Depends(get_db)):
    recipes_likes=db.query(models.Score).filter(models.Score.id_recipe==recipe).filter(models.Score.like==True).all()
    likes = recipes_likes.__len__()
    return likes

#функция подсчёта дизлайков
def dizlikes_recipes(recipe,db:Session=Depends(get_db)):
    recipes_dizlikes=db.query(models.Score).filter(models.Score.id_recipe==recipe).filter(models.Score.dizlike==True).all()
    dizlikes = recipes_dizlikes.__len__()
    return dizlikes

#функция добавления рецептам лайков и дизлайков
def for_recipes(recipe_db,db:Session=Depends(get_db)):
    for recipe in recipe_db:
        recipe.likes=likes_recipes(recipe.id,db)
        recipe.dizlikes=dizlikes_recipes(recipe.id,db)
    return recipe_db


#вывод одного рецепта
@router.get("/{id}", response_model=pyd.RecipeScheme)
async def get_recipes_one(id:int, db:Session=Depends(get_db)):
    recipes_one=db.query(models.Recipe).filter(models.Recipe.id==id).filter(models.Recipe.published==True).first()
    if not recipes_one:
        raise HTTPException(status_code=404, detail="Рецепт не найден!")
    recipes_one.likes=likes_recipes(id,db)
    recipes_one.dizlikes=dizlikes_recipes(id,db)
    return recipes_one

#получение полного списка рецептов
@router.get('/', response_model=List[pyd.RecipeScheme])
async def get_recipes(db:Session=Depends(get_db)):
    query = (
        select(models.Recipe)
        .options(
        selectinload(models.Recipe.steps)
        ))
    res = db.execute(query)
    ress=res.scalars().all()
    for_recipes(ress,db)
    return ress

#читаем рецепты пагинацией
@router.get("/page/all", response_model=Page[pyd.RecipeScheme])
async def get_recipes_all(db:Session=Depends(get_db)):
    recipes_db=db.query(models.Recipe).all()
    for_recipes(recipes_db,db)
    return paginate(recipes_db)

add_pagination(router)

#вывод опубликованных рецептов
@router.get("/page/true", response_model=Page[pyd.RecipeScheme])
async def get_recipes_true(db:Session=Depends(get_db)):
    recipes_true=db.query(models.Recipe).filter(models.Recipe.published==True).all()
    for_recipes(recipes_true,db)
    return paginate(recipes_true)

add_pagination(router)

#вывод неопубликованных рецептов
@router.get("/page/false", response_model=Page[pyd.RecipeScheme])
async def get_recipes_false(db:Session=Depends(get_db)):
    recipes_false=db.query(models.Recipe).filter(models.Recipe.published==False).all()
    for_recipes(recipes_false,db)
    return paginate(recipes_false)

add_pagination(router)

#вывод опубликованных рецептов по категории и времени употребления через query
@router.get("/page/true/category/", response_model=Page[pyd.RecipeScheme])
async def get_recipes_true_category(name: str, db:Session=Depends(get_db)):
    category_db=db.query(models.Category).filter(models.Category.name==name).first()
    if not category_db:
        mealtime_db=db.query(models.Mealtime).filter(models.Mealtime.name==name).first()
        if not mealtime_db:
            raise HTTPException(status_code=404, detail="Категория не найдена!")
        mealtime_recipes_true=db.query(models.Recipe).filter(models.Recipe.published==True).filter(models.Recipe.mealtime.contains(mealtime_db)).all()
        for_recipes(mealtime_recipes_true,db)
        return paginate(mealtime_recipes_true)
    category_recipes_true=db.query(models.Recipe).filter(models.Recipe.published==True).filter(models.Recipe.category==category_db).all()
    for_recipes(category_recipes_true,db)
    return paginate(category_recipes_true)

add_pagination(router)

#вывод картинки
@router.get("/files/{img_name}")
async def get_image(img_name:str, db:Session=Depends(get_db)):
    image_path = Path(f"files/{img_name}")
    if not image_path.is_file():
        return {"error": "Изображение не найдено!"}
    return FileResponse(image_path) 

#добавление рецепта
@router.post('/')
async def create_recipes(recipe_input:pyd.RecipeCreate, step_input:List[pyd.StepCreate], count_input:List[pyd.CountCreate], db:Session=Depends(get_db), payload:dict=Depends(auth_utils.auth_wrapper)):
    #добавление данных в талицу Recipe
    user_db = db.query(models.User).filter(models.User.name==payload.get("username")).first() #находим зарегестрированного сейчас пользователя
    recipe_db=models.Recipe()
    recipe_db.name=recipe_input.name
    #категория - одна
    category_db = db.query(models.Category).filter(models.Category.id==recipe_input.id_category).first()
    if category_db:
        recipe_db.category=category_db #отношение
    else:
        raise HTTPException(status_code=404, detail="Категория не найдена!")
    #пользователь - одна
    recipe_db.user=user_db #обращение конкретно к отношению
    #время приёма пищи  - несколько 
    for id_mealtime in recipe_input.id_mealtime:
        mealtime_db = db.query(models.Mealtime).filter(models.Mealtime.id==id_mealtime).first()
        if mealtime_db:
            recipe_db.mealtime.append(mealtime_db)
        else:
            raise HTTPException(status_code=404, detail="Время приёма пищи не найдено!")
    recipe_db.cooking_time=recipe_input.cooking_time
    db.add(recipe_db)
    #db.commit()

    #добавление данных в таблицу Step
    for step in step_input:
        step_db=models.Step()
        step_db.number=(step_input.index(step)) + 1
        step_db.info=step.info
        step_db.recipe=recipe_db
        db.add(step_db)
        #db.commit()

    #добавление данных в таблицу Count
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
        #db.commit()
    db.commit()
    return "Рецепт отправлен модератору!"

#добавление главного изображения рецепту
@router.post('/img')
async def create_photos(url:str= Depends(upload_file.save_file), db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.name==payload.get("username")).first() #получаем пользователя
    recipe_db = db.query(models.Recipe).filter(models.Recipe.id_user==user_db.id).order_by(models.Recipe.created_at.desc()).first() #находим рецепт, принадлежащий пользователю
    print(url)
    recipe_db.face_img=url
    db.commit()
    return "Изображение добавлено!"

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

#публикация рецепта
@router.put('/published/{recipe_id}')
async def published_recipes(recipe_id:int, db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    recipe_db=db.query(models.Recipe).filter(models.Recipe.id==recipe_id).first()
    if not recipe_db:
        raise HTTPException(status_code=404, detail="Рецепт не найден!")
    if recipe_db.published == True:
        return "Этот рецепт уже опубликован!"
    else: 
        recipe_db.published = True
    db.commit()
    return "Рецепт успешно опубликован!"