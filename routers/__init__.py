# в этом файле подключаются все маршрутизаторы апи, у каждого меняется название
from .category_router import router as category_router
from .ingredient_router import router as ingredient_router
from .mealtime_router import router as mealtime_router
from .recipe_router import router as recipe_router
from .step_router import router as step_router
from .sys_of_calc_router import router as sys_of_calc_router
from .user_router import router as user_router
from .photo_router import router as photo_router