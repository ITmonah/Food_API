from .base_models import *
from typing import List

class RecipeScheme(RecipeBase):
    user:UserBase #связь с рецептами
    category:CategoryBase #связь с категориями
    mealtime:List[MealtimeBase] #связь с временем приёма пищи
    ingredient:List[IngredientBase] #связь с ингредиентами

class Additional_photoScheme(Additional_photoBase):
    recipe_photo:RecipeBase #связь с рецептами

class StepScheme(StepBase):
    recipe:RecipeBase #связь с рецептами