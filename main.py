from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import pyd
from typing import List

app = FastAPI()

#получение списка рецептов
@app.get('/recipes', response_model=List[pyd.RecipeScheme])
async def get_recipes(db:Session=Depends(get_db)):
    recipes=db.query(models.Recipe).all()
    return recipes

#добавление рецепта
@app.post('/recipes', response_model=pyd.RecipeScheme)
async def create_recipes(recipe_input:pyd.RecipeCreate, db:Session=Depends(get_db)):
    recipe_db=models.Recipe()
    recipe_db.name=recipe_input.name
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
@app.put('/recipes/{recipe_id}', response_model=pyd.RecipeScheme)
async def update_recipes(recipe_id:int, recipe_input:pyd.RecipeCreate, db:Session=Depends(get_db)):
    recipe_db=db.query(models.Recipe).filter(models.Recipe.id==recipe_id).first()
    if not recipe_db:
        raise HTTPException(status_code=404, detail="Рецепт не найден!")
    recipe_db.name=recipe_input.name
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

############################################################################

#получение списка ингредиентов
@app.get('/ingredients', response_model=List[pyd.IngredientBase])
async def get_ingredients(db:Session=Depends(get_db)):
    ingredients=db.query(models.Ingredient).all()
    return ingredients
#добавление ингредиента
@app.post('/ingredients', response_model=pyd.IngredientBase)
async def create_ingredients(ingredient_input:pyd.IngredientCreate, db:Session=Depends(get_db)):
    ingredient_db=models.Ingredient()
    ingredient_db.name=ingredient_input.name

    db.add(ingredient_db)
    db.commit()
    return ingredient_db
#редактирование ингредиента
@app.put('/ingredients/{ingredient_id}', response_model=pyd.IngredientBase)
async def update_ingredients(ingredient_id:int, ingredient_input:pyd.IngredientBase, db:Session=Depends(get_db)):
    ingredient_db=db.query(models.Ingredient).filter(models.Ingredient.id==ingredient_id).first()
    if not ingredient_db:
        raise HTTPException(status_code=404, detail="Ингредиент не найден!")
    ingredient_db.name=ingredient_input.name
    db.commit()
    return ingredient_db

############################################################################

#получение списка системы исчисления
@app.get('/system_of_calculations', response_model=List[pyd.System_of_calculationBase])
async def get_system_of_calculations(db:Session=Depends(get_db)):
    system_of_calculations=db.query(models.System_of_calculation).all()
    return system_of_calculations
#добавление системы исчисления
@app.post('/system_of_calculations', response_model=pyd.System_of_calculationBase)
async def create_system_of_calculations(system_of_calculation_input:pyd.System_of_calculationCreate, db:Session=Depends(get_db)):
    system_of_calculation_db=models.System_of_calculation()
    system_of_calculation_db.name=system_of_calculation_input.name

    db.add(system_of_calculation_db)
    db.commit()
    return system_of_calculation_db
#редактирование системы исчисления
@app.put('/system_of_calculations/{system_of_calculation_id}', response_model=pyd.System_of_calculationBase)
async def update_system_of_calculations(system_of_calculation_id:int, system_of_calculation_input:pyd.System_of_calculationBase, db:Session=Depends(get_db)):
    system_of_calculation_db=db.query(models.System_of_calculation).filter(models.System_of_calculation.id==system_of_calculation_id).first()
    if not system_of_calculation_db:
        raise HTTPException(status_code=404, detail="Система исчисления не найдена!")
    system_of_calculation_db.name=system_of_calculation_input.name
    db.commit()
    return system_of_calculation_db

############################################################################

#получение списка категорий
@app.get('/categorys', response_model=List[pyd.CategoryBase])
async def get_categorys(db:Session=Depends(get_db)):
    categorys=db.query(models.Category).all()
    return categorys
#добавление категории
@app.post('/categorys', response_model=pyd.CategoryBase)
async def create_categorys(category_input:pyd.CategoryCreate, db:Session=Depends(get_db)):
    category_db=models.Category()
    category_db.name=category_input.name

    db.add(category_db)
    db.commit()
    return category_db
#редактирование категории
@app.put('/categorys/{category_id}', response_model=pyd.CategoryBase)
async def update_categorys(category_id:int, category_input:pyd.CategoryBase, db:Session=Depends(get_db)):
    category_db=db.query(models.Category).filter(models.Category.id==category_id).first()
    if not category_db:
        raise HTTPException(status_code=404, detail="Категория не найдена!")
    category_db.name=category_input.name
    db.commit()
    return category_db

############################################################################

#получение списка время приёма пищи
@app.get('/mealtimes', response_model=List[pyd.MealtimeBase])
async def get_mealtimes(db:Session=Depends(get_db)):
    mealtimes=db.query(models.Mealtime).all()
    return mealtimes
#добавление времени приёма пищи
@app.post('/mealtimes', response_model=pyd.MealtimeBase)
async def create_mealtimes(mealtime_input:pyd.MealtimeCreate, db:Session=Depends(get_db)):
    mealtime_db=models.Mealtime()
    mealtime_db.name=mealtime_input.name

    db.add(mealtime_db)
    db.commit()
    return mealtime_db
#редактирование времени приёма пищи
@app.put('/mealtimes/{mealtime_id}', response_model=pyd.CategoryBase)
async def update_mealtimes(mealtime_id:int, mealtime_input:pyd.CategoryBase, db:Session=Depends(get_db)):
    mealtime_db=db.query(models.Mealtime).filter(models.Mealtime.id==mealtime_id).first()
    if not mealtime_db:
        raise HTTPException(status_code=404, detail="Время приёма пищи не найдено!")
    mealtime_db.name=mealtime_input.name
    db.commit()
    return mealtime_db


############################################################################

#получение списка шагов
@app.get('/steps', response_model=List[pyd.StepScheme])
async def get_steps(db:Session=Depends(get_db)):
    steps=db.query(models.Step).all()
    return steps
#добавление шага
@app.post('/steps', response_model=pyd.StepScheme)
async def create_steps(step_input:pyd.StepCreate, db:Session=Depends(get_db)):
    step_db=models.Step()
    step_db.number=step_input.number
    step_db.info=step_input.info
    #рецепт - один
    recipe_db = db.query(models.Recipe).filter(models.Recipe.id==step_input.id_recipe).first()
    if recipe_db:
        step_db.recipe=recipe_db #отношение
    else:
        raise HTTPException(status_code=404, detail="Рецепт не найден!")
    db.add(step_db)
    db.commit()
    return step_db
#редактирование шага
@app.put('/steps/{step_id}', response_model=pyd.StepScheme)
async def update_steps(step_id:int, step_input:pyd.StepCreate, db:Session=Depends(get_db)):
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