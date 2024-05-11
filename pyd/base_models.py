from sqlalchemy import DateTime
from pydantic import BaseModel, Field #настройка валидации

class UserBase(BaseModel):
    id:int=Field(...,gt=0,example=228) #обязательно к заполнению
    name:str=Field(...,example="Jin")
    mail:str=Field(...,example="recipes228@mail.ru")
    #img_avatar:
    password:str=Field(...,example="fafal1")
    mailing:bool=Field(...,example=False)
    #data_of_creation:=Field(...,example="20.04.2020")
    class Config:
        orm_mode=True #наша модель будет легко соедняться с бд

class RecipeBase(BaseModel):
    id:int=Field(...,gt=0,example=22) #обязательно к заполнению
    name:str=Field(...,example="Мясо с морковкой")
    #face_img
    #data_of_creation
    cooking_time:int=Field(..., gt=0, example=3) #время готовки
    like:int=Field(..., ge=0, example=3)
    dizlike:int=Field(..., ge=0, example=3)
    views:int=Field(..., ge=0, example=3)
    class Config:
        orm_mode=True #наша модель будет легко соедняться с бд

class IngredientBase(BaseModel):
    id:int=Field(...,gt=0,example=28) #обязательно к заполнению
    name:str=Field(...,example="Морковка")
    class Config:
        orm_mode=True #наша модель будет легко соедняться с бд

class System_of_calculationBase(BaseModel):
    id:int=Field(...,gt=0,example=228) #обязательно к заполнению
    name:str=Field(...,example="Кг")
    class Config:
        orm_mode=True #наша модель будет легко соедняться с бд

class CategoryBase(BaseModel):
    id:int=Field(...,gt=0,example=228) #обязательно к заполнению
    name:str=Field(...,example="Десерт")
    class Config:
        orm_mode=True #наша модель будет легко соедняться с бд

class MealtimeBase(BaseModel):
    id:int=Field(...,gt=0,example=228) #обязательно к заполнению
    name:str=Field(...,example="Ужин")
    class Config:
        orm_mode=True #наша модель будет легко соедняться с бд

class Additional_photoBase(BaseModel):
    id:int=Field(...,gt=0,example=228) #обязательно к заполнению
    #img
    class Config:
        orm_mode=True #наша модель будет легко соедняться с бд

class StepBase(BaseModel):
    id:int=Field(...,gt=0,example=228) #обязательно к заполнению
    number:int=Field(...,gt=0,example=2)
    info:str=Field(...,example="Порезать колабсу и сыр на кубики.")
    class Config:
        orm_mode=True #наша модель будет легко соедняться с бд



