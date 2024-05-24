from pydantic import EmailStr,BaseModel, Field, FileUrl #какой формат данных хотим от пользователя
from typing import List, Dict

class UserCreate(BaseModel):
    name:str=Field(...,max_length=255, min_length=1,example="Jin")
    mail:EmailStr = Field(...,example="recipes228@mail.ru")
    password:str=Field(...,max_length=255, min_length=6,example="fafal1")

class UserEditingImg(BaseModel): #класс для редактирования фото пользователя
    img_avatar:str=Field(...,example="files/hh.png")

class UserEditingMail(BaseModel): #класс для редактирования почты пользователя
    mail:EmailStr = Field(...,example="recipes228@mail.ru")

class UserEditingMailing(BaseModel): #класс для редактирования рассылки пользователя
    mailing:bool=Field(...,example=False)

class UserEditingPass(BaseModel): #класс для редактирования пароля пользователя
    password:str=Field(...,max_length=255, min_length=6,example="fafal1")

class RecipeCreate(BaseModel):
    name:str=Field(...,max_length=255, min_length=1,example="Чизкейк")
    #face_img:str=Field(...,example="files/hh.png")
    id_category:int=Field(..., gt=0, example=10)
    #id_user:int=Field(..., gt=0, example=10)
    cooking_time:int=Field(..., gt=0, example=2) #время готовки
    id_mealtime:List[int] = None #для добавления времени приготовления через запятую
    id_ingredient:List[int] = None

class IngredientCreate(BaseModel):
    name:str=Field(...,max_length=255, min_length=1,example="Морковка")

class System_of_calculationCreate(BaseModel):
    name:str=Field(...,max_length=255, min_length=1,example="Кг")

class Count(BaseModel):
    count:int=Field(..., gt=0, example=10)

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
    info:str=Field(...,max_length=255, min_length=1,example="Порезать колбасу и сыр на кубики.")
    #id_recipe:int=Field(...,gt=0,example=1)

class Credentials(BaseModel):
    mail: EmailStr = Field(..., example='recipes221@mail.ru')
    pwd: str = Field(..., max_length=255, min_length=6, example='123456')