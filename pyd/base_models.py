from datetime import date, datetime
from pydantic import EmailStr, BaseModel, Field, FileUrl #настройка валидации

class UserBase(BaseModel):
    id:int=Field(...,gt=0,example=228) #обязательно к заполнению
    name:str=Field(...,example="Jin")
    mail:EmailStr = Field(...,example="recipes228@mail.ru")
    img_avatar:str=Field(...,example="files/hh.png")
    mailing:bool=Field(...,example=False)
    created_at:datetime=Field(...,example='2001-01-01 00:00:00')
    email_verify:bool=Field(...)
    class Config:
        orm_mode=True #наша модель будет легко соедняться с бд

class RecipeBase(BaseModel):
    id:int=Field(...,gt=0,example=22) #обязательно к заполнению
    name:str=Field(...,example="Мясо с морковкой")
    face_img:str=Field(...,example="files/hh.png")
    created_at:datetime=Field(...,example='2001-01-01 00:00:00')
    cooking_time:int=Field(..., gt=0, example=3) #время готовки
    views:int=Field(..., ge=0, example=3)
    published:bool=Field(..., example=False) #публикация
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
    img:str=Field(...,example="files/hh.png")
    class Config:
        orm_mode=True #наша модель будет легко соедняться с бд

class StepBase(BaseModel):
    id:int=Field(...,gt=0,example=228) #обязательно к заполнению
    number:int=Field(...,gt=0,example=2)
    info:str=Field(...,example="Порезать колабсу и сыр на кубики.")
    class Config:
        orm_mode=True #наша модель будет легко соедняться с бд

class CountBase(BaseModel): #таблица, связывающая ингредиенты и рецепты
    id:int=Field(...,gt=0,example=228) #обязательно к заполнению     
    count:int=Field(...,gt=0,example=228)
    class Config:
            orm_mode=True #наша модель будет легко соедняться с бд

class ScoreBase(BaseModel): #таблица лайков и дизлайков
    id:int=Field(...,gt=0,example=228) #обязательно к заполнению     
    like:bool=Field(...,ge=0,example=False)
    dizlike:bool=Field(...,ge=0,example=False)
    class Config:
            orm_mode=True #наша модель будет легко соедняться с бд