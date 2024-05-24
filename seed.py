from sqlalchemy.orm import Session
from database import engine
import models

models.Base.metadata.drop_all(bind=engine) #пересоздание таблиц
models.Base.metadata.create_all(bind=engine) #пересоздание таблиц

with Session(bind=engine) as session:
    #123456 и qwerty
    u1=models.User(name="Малинина", mail="recipes228@mail.ru",img_avatar="http://127.0.0.1:8000/recipe/files/food.png", password="$2b$12$/2gx.pO8GYYk7yASJfH3m.rYwOgaO/GvZ6Mzvqvyq.ZdT/mnZBpRS", mailing=False, email_verify=1) #пользователи
    u2=models.User(name="Хомяк", mail="recipes223@mail.ru",img_avatar="http://127.0.0.1:8000/recipe/files/food.png", password="$2b$12$o3y6j3I0lS/MqDQ79AxSG.hZIBKC9JyYOUYeIaQh1lCsYeRWKzg9i", mailing=False, email_verify=1)
    
    i1=models.Ingredient(name="Шоколад") #ингредиенты
    i2=models.Ingredient(name="Картошка")
    i3=models.Ingredient(name="Клубника")
    i4=models.Ingredient(name="Сыр")
    i5=models.Ingredient(name="Колбаса")

    soc1=models.System_of_calculation(name="Кг") #система исчисления
    soc2=models.System_of_calculation(name="Г")
    soc3=models.System_of_calculation(name="Л")
    soc4=models.System_of_calculation(name="Мл")
    soc5=models.System_of_calculation(name="Шт")

    c1=models.Category(name="Десерт") #категории
    c2=models.Category(name="Мясо")
    c3=models.Category(name="Суп")
    c4=models.Category(name="Рыба")
    c5=models.Category(name="Напиток")
    c6=models.Category(name="Основное")

    m1=models.Mealtime(name="Завтрак") #время приёма пищи
    m2=models.Mealtime(name="Обед")
    m3=models.Mealtime(name="Ужин")

    r1=models.Recipe(name="Пицца", face_img="http://127.0.0.1:8000/recipe/files/pizza.jpg", cooking_time=3, category=c6, user=u1, mealtime=[m2,m3],ingredient=[i4,i5]) #рецепты

    s1=models.Step(number=1, info="Потрите сыр на тёрке", recipe=r1) #шаги
    s2=models.Step(number=2, info="Порежьте колбасу на кубики", recipe=r1) #шаги

    ap1=models.Additional_photo(recipe_photo=r1, img="http://127.0.0.1:8000/recipe/files/pizza2.jpg") #дополнительные фото

    session.add_all([u1,u2, i1,i2,i3,i4,i5, soc1,soc2,soc3,soc4,soc5, c1,c2,c3,c4,c5,c6, m1,m2,m3, r1, s1,s2, ap1])
    session.commit()

