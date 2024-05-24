from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from routers import category_router, ingredient_router, mealtime_router, recipe_router, step_router, sys_of_calc_router, user_router, photo_router
#модули для связи бэка с фронтом
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

app = FastAPI()

# подключение АпиРоутера (маршруты сущности)
app.include_router(user_router)
app.include_router(recipe_router)
app.include_router(step_router)
app.include_router(photo_router)

app.include_router(category_router)
app.include_router(ingredient_router)
app.include_router(mealtime_router)
app.include_router(sys_of_calc_router)

#управление CORS - совместное использование ресурсов разных источников
origins=["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)