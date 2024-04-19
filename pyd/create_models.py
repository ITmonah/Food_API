from pydantic import BaseModel, Field #какой формат данных хотим от пользователя
from typing import List
from sqlalchemy import DateTime

class UserCreate(BaseModel):
    name:str=Field(...,max_length=255, min_length=1,example="Jin")
    mail:str=Field(...,example="recipes228@mail.ru")
    #img_avatar:
    password:str=Field(...,max_length=255, min_length=1,example="fafal1")
    mailing:bool=Field(...,example=False)
    #data_of_creation:=Field(...,example="20.04.2020")

class RecipeCreate(BaseModel):
    name:str=Field(...,max_length=255, min_length=1,example="Jin")
    #face_img
    id_category:int=Field(..., gt=0, example=10)
    id_user:int=Field(..., gt=0, example=10)
    #data_of_creation
    cooking_time:int=Field(..., gt=0, example=2) #время готовки
    id_mealtime:List[int] = None #для добавления времени приготовления через запятую
    id_ingredient:List[int] = None

class IngredientCreate(BaseModel):
    name:str=Field(...,max_length=255, min_length=1,example="Морковка")

class System_of_calculationCreate(BaseModel):
    name:str=Field(...,max_length=255, min_length=1,example="Кг")

class CategoryCreate(BaseModel):
    name:str=Field(...,max_length=255, min_length=1,example="Десерт")

class MealtimeCreate(BaseModel):
    name:str=Field(...,max_length=255, min_length=1,example="Ужин")

class Additional_photoCreate(BaseModel):
    id:int=Field(...,gt=0,example=228) #обязательно к заполнению
    #img
    id_recipe:int=Field(...,gt=0,example=1)

class StepCreate(BaseModel):
    number:int=Field(...,gt=0,example=2)
    info:str=Field(...,max_length=255, min_length=1,example="Порезать колабсу и сыр на кубики.")
    id_recipe:int=Field(...,gt=0,example=1)

