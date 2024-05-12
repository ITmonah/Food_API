from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from routers import category_router, ingredient_router, mealtime_router, recipe_router, step_router, sys_of_calc_router, user_router

app = FastAPI()

# подключение АпиРоутера (маршруты сущности)
app.include_router(category_router)
app.include_router(ingredient_router)
app.include_router(mealtime_router)
app.include_router(recipe_router)
app.include_router(step_router)
app.include_router(sys_of_calc_router)
app.include_router(user_router)
