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
        recipe.raiting= recipe.likes * 2 - recipe.dizlikes
        if recipe.raiting < 0:
            recipe.raiting=0
    return recipe_db


#вывод одного рецепта
@router.get("/{id}", response_model=pyd.RecipeScheme)
async def get_recipes_one(id:int, db:Session=Depends(get_db)):
    recipes_one=db.query(models.Recipe).filter(models.Recipe.id==id).filter(models.Recipe.published==True).first()
    if not recipes_one:
        raise HTTPException(status_code=404, detail="Рецепт не найден!")
    recipes_one.likes=likes_recipes(id,db)
    recipes_one.dizlikes=dizlikes_recipes(id,db)
    recipes_one.raiting= recipes_one.likes * 2 - recipes_one.dizlikes
    if recipes_one.raiting < 0:
        recipes_one.raiting=0
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

#вывод топ-3 рецептов по рейтингу
@router.get("/top/", response_model=List[pyd.RecipeScheme])
async def get_recipes_top(db:Session=Depends(get_db)):
    recipes_true=db.query(models.Recipe).filter(models.Recipe.published==True).all()
    for_recipes(recipes_true,db)
    sorted_recipes = sorted(recipes_true, key=lambda x: x.raiting, reverse=True)
    return sorted_recipes[0],sorted_recipes[1],sorted_recipes[2]

#читаем рецепты пагинацией
@router.get("/page/all", response_model=Page[pyd.RecipeScheme])
async def get_recipes_all(db:Session=Depends(get_db)):
    recipes_db=db.query(models.Recipe).all()
    for_recipes(recipes_db,db)
    return paginate(recipes_db)

add_pagination(router)

#вывод опубликованных рецептов с сортировкой
@router.get("/page/true", response_model=Page[pyd.RecipeScheme]) 
async def get_recipes_true(sort:str, db:Session=Depends(get_db)):
    if sort == "created_at":
        recipes_true=db.query(models.Recipe).filter(models.Recipe.published==True).order_by(models.Recipe.created_at.desc()).all()
        for_recipes(recipes_true,db)
        return paginate(recipes_true)
    if sort == "cooking_time" : 
        recipes_true=db.query(models.Recipe).filter(models.Recipe.published==True).order_by(models.Recipe.cooking_time.asc()).all()
        for_recipes(recipes_true,db)
        return paginate(recipes_true)
    if sort == "raiting":
        recipes_true=db.query(models.Recipe).filter(models.Recipe.published==True).all()
        for_recipes(recipes_true,db)
        sorted_recipes = sorted(recipes_true, key=lambda x: x.raiting, reverse=True)
        return paginate(sorted_recipes)
    else:
        raise HTTPException(status_code=404, detail="Указана неверная сортировка!") 

add_pagination(router)

#вывод неопубликованных рецептов
@router.get("/page/false", response_model=Page[pyd.RecipeScheme]) #только админ
async def get_recipes_false(db:Session=Depends(get_db), payload:dict=Depends(auth_utils.auth_wrapper)):
    if payload.get("username") == "edok228":
        recipes_false=db.query(models.Recipe).filter(models.Recipe.published==False).all()
        for_recipes(recipes_false,db)
        return paginate(recipes_false)
    else:
        raise HTTPException(status_code=404, detail="Вы не администратор!")

add_pagination(router)

#вывод опубликованных рецептов по категории и времени употребления через query
@router.get("/page/true/category/", response_model=Page[pyd.RecipeScheme]) 
async def get_recipes_true_category(name: str, sort: str, db:Session=Depends(get_db)):
    category_db=db.query(models.Category).filter(models.Category.name==name).first()
    if not category_db:
        mealtime_db=db.query(models.Mealtime).filter(models.Mealtime.name==name).first()
        if not mealtime_db:
            raise HTTPException(status_code=404, detail="Категория не найдена!")
        mealtime_recipes_true=db.query(models.Recipe).filter(models.Recipe.published==True).filter(models.Recipe.mealtime.contains(mealtime_db)).all()
        for_recipes(mealtime_recipes_true,db)
        if sort == "created_at":
            sorted_recipes = sorted(mealtime_recipes_true, key=lambda x: x.created_at, reverse=True)
            return paginate(sorted_recipes)
        if sort == "cooking_time" : 
            sorted_recipes = sorted(mealtime_recipes_true, key=lambda x: x.cooking_time, reverse=False)
            return paginate(sorted_recipes)
        if sort == "raiting":
            sorted_recipes = sorted(mealtime_recipes_true, key=lambda x: x.raiting, reverse=True)
            return paginate(sorted_recipes)
        return paginate(mealtime_recipes_true)
    category_recipes_true=db.query(models.Recipe).filter(models.Recipe.published==True).filter(models.Recipe.category==category_db).all()
    for_recipes(category_recipes_true,db)
    if sort == "created_at":
        sorted_recipes = sorted(category_recipes_true, key=lambda x: x.created_at, reverse=True)
        return paginate(sorted_recipes)
    if sort == "cooking_time" : 
        sorted_recipes = sorted(category_recipes_true, key=lambda x: x.cooking_time, reverse=False)
        return paginate(sorted_recipes)
    if sort == "raiting":
        sorted_recipes = sorted(category_recipes_true, key=lambda x: x.raiting, reverse=True)
        return paginate(sorted_recipes)
    return paginate(category_recipes_true)

add_pagination(router)

#вывод опубликованных рецептов по названию рецепта через query
@router.get("/page/true/search/", response_model=Page[pyd.RecipeScheme])
async def get_recipes_true_search(name: str, db:Session=Depends(get_db)):
    name = name.lower()
    recipes_first=db.query(models.Recipe).filter(models.Recipe.published==True).filter(models.Recipe.name.contains(name)).order_by(models.Recipe.name.asc()).all()
    name = name[0].upper() + name[1:]
    recipes_second=db.query(models.Recipe).filter(models.Recipe.published==True).filter(models.Recipe.name.contains(name)).order_by(models.Recipe.name.asc()).all()
    recipes = recipes_second+recipes_first
    for_recipes(recipes,db)
    return paginate(recipes)

add_pagination(router)

#вывод опубликованных рецептов по названию рецепта через query с категорией
@router.get("/page/true/search/category", response_model=Page[pyd.RecipeScheme])
async def get_recipes_true_search_category(name: str, cat: str, db:Session=Depends(get_db)):
    name = name.lower()
    category_db=db.query(models.Category).filter(models.Category.name==cat).first()
    if not category_db:
        mealtime_db=db.query(models.Mealtime).filter(models.Mealtime.name==cat).first()
        if not mealtime_db:
            raise HTTPException(status_code=404, detail="Категория не найдена!")
        #время приготовления
        mealtime_recipes_true=db.query(models.Recipe).filter(models.Recipe.published==True).filter(models.Recipe.mealtime.contains(mealtime_db)).filter(models.Recipe.name.contains(name)).order_by(models.Recipe.name.asc()).all()
        #поиск 
        name = name[0].upper() + name[1:]
        recipes_second=db.query(models.Recipe).filter(models.Recipe.published==True).filter(models.Recipe.mealtime.contains(mealtime_db)).filter(models.Recipe.name.contains(name)).order_by(models.Recipe.name.asc()).all()
        recipes = recipes_second+mealtime_recipes_true
        for_recipes(recipes,db)
        return paginate(recipes)
    #категория
    category_recipes_true=db.query(models.Recipe).filter(models.Recipe.published==True).filter(models.Recipe.category==category_db).filter(models.Recipe.name.contains(name)).order_by(models.Recipe.name.asc()).all()
    #поиск
    name = name[0].upper() + name[1:]
    recipes_second=db.query(models.Recipe).filter(models.Recipe.published==True).filter(models.Recipe.category==category_db).filter(models.Recipe.name.contains(name)).order_by(models.Recipe.name.asc()).all()
    recipes = recipes_second+category_recipes_true
    for_recipes(recipes,db)
    return paginate(recipes)

add_pagination(router)

#вывод опубликованных рецептов по названию рецепта через query с сортировкой
@router.get("/page/true/search/sort", response_model=Page[pyd.RecipeScheme])
async def get_recipes_true_search_sort(name: str, sort: str, db:Session=Depends(get_db)):
    name = name.lower()
    recipes_first=db.query(models.Recipe).filter(models.Recipe.published==True).filter(models.Recipe.name.contains(name)).order_by(models.Recipe.name.asc()).all()
    name = name[0].upper() + name[1:]
    recipes_second=db.query(models.Recipe).filter(models.Recipe.published==True).filter(models.Recipe.name.contains(name)).order_by(models.Recipe.name.asc()).all()
    recipes = recipes_second+recipes_first
    for_recipes(recipes,db)
    if sort == "created_at":
        sorted_recipes = sorted(recipes, key=lambda x: x.created_at, reverse=True)
        return paginate(sorted_recipes)
    if sort == "cooking_time" : 
        sorted_recipes = sorted(recipes, key=lambda x: x.cooking_time, reverse=False)
        return paginate(sorted_recipes)
    if sort == "raiting":
        sorted_recipes = sorted(recipes, key=lambda x: x.raiting, reverse=True)
        return paginate(sorted_recipes)
    return paginate(recipes)

add_pagination(router)

#вывод опубликованных рецептов по названию рецепта через query с сортировкой и с категорией
@router.get("/page/true/search/sort/category", response_model=Page[pyd.RecipeScheme])
async def get_recipes_true_search_sort_category(name: str, cat:str, sort: str, db:Session=Depends(get_db)):
    name = name.lower()
    category_db=db.query(models.Category).filter(models.Category.name==cat).first()
    if not category_db:
        mealtime_db=db.query(models.Mealtime).filter(models.Mealtime.name==cat).first()
        if not mealtime_db:
            raise HTTPException(status_code=404, detail="Категория не найдена!")
        #время приготовления
        mealtime_recipes_true=db.query(models.Recipe).filter(models.Recipe.published==True).filter(models.Recipe.mealtime.contains(mealtime_db)).filter(models.Recipe.name.contains(name)).order_by(models.Recipe.name.asc()).all()
        #поиск 
        name = name[0].upper() + name[1:]
        recipes_second=db.query(models.Recipe).filter(models.Recipe.published==True).filter(models.Recipe.mealtime.contains(mealtime_db)).filter(models.Recipe.name.contains(name)).order_by(models.Recipe.name.asc()).all()
        recipes = recipes_second+mealtime_recipes_true
        for_recipes(recipes,db)
        if sort == "created_at":
            sorted_recipes = sorted(recipes, key=lambda x: x.created_at, reverse=True)
            return paginate(sorted_recipes)
        if sort == "cooking_time" : 
            sorted_recipes = sorted(recipes, key=lambda x: x.cooking_time, reverse=False)
            return paginate(sorted_recipes)
        if sort == "raiting":
            sorted_recipes = sorted(recipes, key=lambda x: x.raiting, reverse=True)
            return paginate(sorted_recipes)
        return paginate(recipes)
    #категория
    category_recipes_true=db.query(models.Recipe).filter(models.Recipe.published==True).filter(models.Recipe.category==category_db).filter(models.Recipe.name.contains(name)).order_by(models.Recipe.name.asc()).all()
    #поиск
    name = name[0].upper() + name[1:]
    recipes_second=db.query(models.Recipe).filter(models.Recipe.published==True).filter(models.Recipe.category==category_db).filter(models.Recipe.name.contains(name)).order_by(models.Recipe.name.asc()).all()
    recipes = recipes_second+category_recipes_true
    for_recipes(recipes,db)
    if sort == "created_at":
        sorted_recipes = sorted(recipes, key=lambda x: x.created_at, reverse=True)
        return paginate(sorted_recipes)
    if sort == "cooking_time" : 
        sorted_recipes = sorted(recipes, key=lambda x: x.cooking_time, reverse=False)
        return paginate(sorted_recipes)
    if sort == "raiting":
        sorted_recipes = sorted(recipes, key=lambda x: x.raiting, reverse=True)
        return paginate(sorted_recipes)
    return paginate(recipes)

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
    user_db = db.query(models.User).filter(models.User.name==payload.get("username")).first() #находим зарегистрированного сейчас пользователя
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
        count_db.recipe=recipe_db #добавление рецепт
        ing_db=db.query(models.Ingredient).filter(models.Ingredient.id==count_int.id_ingredient).first() 
        if not ing_db:
            raise HTTPException(status_code=404, detail="Ингредиент не найден!")
        count_db.id_ingredient=ing_db.id
        count_db.count=count_int.count
        sys_db=db.query(models.System_of_calculation).filter(models.System_of_calculation.id==count_int.id_system_of_calc).first() 
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
    recipe_db.face_img=url
    db.commit()
    return "Изображение добавлено!"

#редактирование рецепта
@router.put('/{recipe_id}', response_model=pyd.RecipeScheme)
async def update_recipes(recipe_id:int,recipe_input:pyd.RecipeCreate, step_input:List[pyd.StepCreate], count_input:List[pyd.CountCreate], db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    user_db = db.query(models.User).filter(models.User.name==payload.get("username")).first() #получаем пользователя
    recipe_db = db.query(models.Recipe).filter(models.Recipe.id_user==user_db.id).filter(models.Recipe.id==recipe_id).first() #находим рецепт, принадлежащий пользователю
    if not recipe_db:
        raise HTTPException(status_code=404, detail="Рецепт не найден!")
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
    recipe_db.mealtime.clear()
    for id_mealtime in recipe_input.id_mealtime:
        mealtime_db = db.query(models.Mealtime).filter(models.Mealtime.id==id_mealtime).first()
        if mealtime_db:
            recipe_db.mealtime.append(mealtime_db)
        else:
            raise HTTPException(status_code=404, detail="Время приёма пищи не найдено!")
    recipe_db.cooking_time=recipe_input.cooking_time
    db.add(recipe_db)
    #db.commit()

    #удаление предыдущих шагов
    db.query(models.Step).filter(models.Step.id_recipe==recipe_id).delete()
    #добавление данных в таблицу Step
    for step in step_input:
        step_db=models.Step()
        step_db.number=(step_input.index(step)) + 1
        step_db.info=step.info
        step_db.recipe=recipe_db
        db.add(step_db)
        #db.commit()
        
    #удаление количества
    db.query(models.Count).filter(models.Count.id_recipe==recipe_id).delete()
    #добавление данных в таблицу Count
    for count_int in count_input:
        count_db=models.Count()
        count_db.recipe=recipe_db #добавление рецепт
        ing_db=db.query(models.Ingredient).filter(models.Ingredient.id==count_int.id_ingredient).first() 
        if not ing_db:
            raise HTTPException(status_code=404, detail="Ингредиент не найден!")
        count_db.id_ingredient=ing_db.id
        count_db.count=count_int.count
        sys_db=db.query(models.System_of_calculation).filter(models.System_of_calculation.id==count_int.id_system_of_calc).first() 
        if not sys_db:
            raise HTTPException(status_code=404, detail="Система исчисления не найдена!")
        count_db.id_system_of_calc = sys_db.id
        db.add(count_db)
        #db.commit()
    db.commit()
    return recipe_db

#удаление рецепта
@router.delete('/{recipe_id}') #только админ
async def delete_recipes(recipe_id:int, db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    if payload.get("username") == "edok228":
        recipe_db=db.query(models.Recipe).filter(models.Recipe.id==recipe_id).first()
        if not recipe_db:
            raise HTTPException(status_code=404, detail="Рецепт не найден!")
        db.delete(recipe_db)
        #удаление шагов
        db.query(models.Step).filter(models.Step.id_recipe==recipe_id).delete()
        #удаление дополнительных фото
        db.query(models.Additional_photo).filter(models.Additional_photo.id_recipe==recipe_id).delete()
        #удаление количества
        db.query(models.Count).filter(models.Count.id_recipe==recipe_id).delete()
        #удаление оценок
        db.query(models.Score).filter(models.Score.id_recipe==recipe_id).delete()
        recipes=db.query(models.Recipe).all()
        a=0
        #удаление фотографии из папки
        for recipe in recipes:
            if recipe.face_img == recipe_db.face_img:
                a=a+1
        if a == 1:
            url = str(recipe_db.face_img)
            Path.unlink(url[7:]) 
        db.commit()
        return "Удаление рецепта прошло успешно!"
    else:
        raise HTTPException(status_code=404, detail="Вы не администратор!")

#публикация рецепта
@router.put('/published/{recipe_id}') #только админ
async def published_recipes(recipe_id:int, db:Session=Depends(get_db),payload:dict=Depends(auth_utils.auth_wrapper)):
    if payload.get("username") == "edok228":
        recipe_db=db.query(models.Recipe).filter(models.Recipe.id==recipe_id).first()
        if not recipe_db:
            raise HTTPException(status_code=404, detail="Рецепт не найден!")
        if recipe_db.published == True:
            return "Этот рецепт уже опубликован!"
        else: 
            recipe_db.published = True
            recipe_db.created_at = func.now()
        db.commit()
        return "Рецепт успешно опубликован!"
    else:
        raise HTTPException(status_code=404, detail="Вы не администратор!")