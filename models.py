from sqlalchemy import Table, Boolean, Column, ForeignKey, Integer, String, DateTime,LargeBinary
from sqlalchemy.orm import relationship #связь между таблицами
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import EmailType
import datetime
#from sqlalchemy_imageattach.entity import Image, image_attachment #библиотека для изображений

from database import Base

ingredients_recipes=Table('ingredient_recipe', Base.metadata, #таблица, связывающая ингредиенты и рецепты
               Column('id', Integer, primary_key=True),           
               Column('id_ingredient', ForeignKey('ingredients.id'), nullable=False, default=2),
               Column('id_recipe', ForeignKey('recipes.id'), nullable=False, default=2),
               Column('count', Integer, nullable=False, default=20),
               Column('id_system_of_calc', ForeignKey('system_of_calculations.id'), nullable=False, default=1))

Mealtime_recipes=Table('mealtime_recipe', Base.metadata, #таблица, связывающая время приготовления еды и рецепты
               Column('id', Integer, primary_key=True),           
               Column('id_mealtime', ForeignKey('mealtimes.id'), nullable=False, default=3),
               Column('id_recipe', ForeignKey('recipes.id'), nullable=False, default=2))

class User(Base): #пользователи
    __tablename__ = "users"

    id = Column(Integer, primary_key=True) #первичный ключ
    name = Column(String(255), nullable=False)
    mail = Column(EmailType, nullable=False)
    #img_avatar = Column(LargeBinary, nullable=True) #фото может не быть
    password = Column(String(255), nullable=False)
    mailing = Column(Boolean, default=False)
    #data_of_creation=Column(DateTime, nullable=False)

class Recipe(Base): #рецепты
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True) #первичный ключ
    name = Column(String(255), nullable=False)
    #face_img = Column(LargeBinary, nullable=False) #фото обязательно
    id_category = Column(Integer, ForeignKey("categories.id"), nullable=False, default=2) #внешний ключ
    id_user = Column(Integer, ForeignKey("users.id"), nullable=False, default=2) #внешний ключ
    #data_of_creation=Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    cooking_time=Column(Integer, nullable=False)
    like=Column(Integer, nullable=False, default=0)
    dizlike=Column(Integer, nullable=False,default=0)
    views=Column(Integer, nullable=False,default=0)

    user=relationship("User", backref="recipes") #обратная связь
    category=relationship("Category", backref="recipes") #обратная связь
    mealtime=relationship("Mealtime", secondary='mealtime_recipe', backref='recipes') #время приготовления
    ingredient=relationship("Ingredient", secondary='ingredient_recipe', backref='recipes') #ингредиенты

class Ingredient(Base): #ингредиенты
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True) #первичный ключ
    name = Column(String(255), nullable=False)

class System_of_calculation(Base): #система исчисления
    __tablename__ = "system_of_calculations"

    id = Column(Integer, primary_key=True) #первичный ключ
    name = Column(String(255), nullable=False)

class Category(Base): #категории еды
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True) #первичный ключ
    name = Column(String(255), nullable=False)

class Mealtime(Base): #время приёма пищи
    __tablename__ = "mealtimes"

    id = Column(Integer, primary_key=True) #первичный ключ
    name = Column(String(255), nullable=False)

class Additional_photo(Base): #дополнительные фото
    __tablename__ = "additional_photos"

    id = Column(Integer, primary_key=True) #первичный ключ
    #img = Column(LargeBinary, nullable=False) #фото обязательно
    id_recipe = Column(Integer, ForeignKey("recipes.id"), nullable=False, default=2) #внешний ключ

    recipe_photo=relationship("Recipe", backref="additional_photos") #обратная связь

class Step(Base): #шаги рецепта
    __tablename__ = "steps"

    id = Column(Integer, primary_key=True) #первичный ключ
    number = Column(Integer, default=1) 
    info = Column(String(255), nullable=False)
    id_recipe = Column(Integer, ForeignKey("recipes.id"), nullable=False, default=2) #внешний ключ

    recipe=relationship("Recipe", backref="steps") #обратная связь

