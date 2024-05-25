from sqlalchemy.orm import Session
from database import engine
import models

models.Base.metadata.drop_all(bind=engine) #пересоздание таблиц
models.Base.metadata.create_all(bind=engine) #пересоздание таблиц

with Session(bind=engine) as session:
    #123456 и qwerty
    u1=models.User(name="Малинина", mail="recipes228@mail.ru",img_avatar="http://127.0.0.1:8000/recipe/files/food.png", password="$2b$12$/2gx.pO8GYYk7yASJfH3m.rYwOgaO/GvZ6Mzvqvyq.ZdT/mnZBpRS", mailing=False, email_verify=1) #пользователи
    u2=models.User(name="Хомяк", mail="recipes223@mail.ru",img_avatar="http://127.0.0.1:8000/recipe/files/food.png", password="$2b$12$o3y6j3I0lS/MqDQ79AxSG.hZIBKC9JyYOUYeIaQh1lCsYeRWKzg9i", mailing=False, email_verify=1)
    u3=models.User(name="edok228", mail="admin@mail.ru",img_avatar="http://127.0.0.1:8000/recipe/files/food.png", password="$2b$12$3/w7zRoYtYe4344FtJtlRuKDkfLAiZd3XqZaHaxn1zJ/DFcG/Brs6", mailing=True, email_verify=1)
    
    i1=models.Ingredient(name="Шоколад") #ингредиенты
    i2=models.Ingredient(name="Картошка")
    i3=models.Ingredient(name="Клубника")
    i4=models.Ingredient(name="Сыр")
    i5=models.Ingredient(name="Колбаса")
    i6=models.Ingredient(name="Молоко")
    i7=models.Ingredient(name="Малина")

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

    r1=models.Recipe(name="Пицца", face_img="http://127.0.0.1:8000/recipe/files/pizza.jpg", cooking_time=45, category=c6, user=u1, mealtime=[m2,m3],ingredient=[i4,i5], published=False) #рецепты
    r2=models.Recipe(name="Клубника в шоколаде", face_img="http://127.0.0.1:8000/recipe/files/choko.jpg", cooking_time=15, category=c1, user=u1, mealtime=[m1],ingredient=[i1,i2],published=True) 
    r3=models.Recipe(name="Макароны с сыром", face_img="http://127.0.0.1:8000/recipe/files/mak.jpg", cooking_time=20, category=c6, user=u2, mealtime=[m2,m3],ingredient=[i4],published=True) 
    r4=models.Recipe(name="Гречка с молоком", face_img="http://127.0.0.1:8000/recipe/files/grechka.jpg", cooking_time=20, category=c6, user=u1, mealtime=[m1,m2,m3],ingredient=[i6],published=False) 
    r5=models.Recipe(name="Чай с малиной", face_img="http://127.0.0.1:8000/recipe/files/chay.png", cooking_time=10, category=c5, user=u2, mealtime=[m1,m2,m3],ingredient=[i7],published=True) 

    s1=models.Step(number=1, info="Потрите сыр на тёрке", recipe=r1) #шаги
    s2=models.Step(number=2, info="Порежьте колбасу на кубики", recipe=r1) 
    s3=models.Step(number=1, info="Окуните клубнику в шоколад", recipe=r2)
    s4=models.Step(number=1, info="Отварите макароны", recipe=r3)
    s5=models.Step(number=2, info="Посыпьте тёртым сыром", recipe=r3)
    s6=models.Step(number=1, info="Залейте гручку молоком", recipe=r4)
    s7=models.Step(number=1, info="Положите малину в чай и дайте напитку настояться", recipe=r5)

    ap1=models.Additional_photo(recipe_photo=r1, img="http://127.0.0.1:8000/recipe/files/pizza2.jpg") #дополнительные фото
    ap2=models.Additional_photo(recipe_photo=r2, img="http://127.0.0.1:8000/recipe/files/choko2.jpg") 
    ap3=models.Additional_photo(recipe_photo=r3, img="http://127.0.0.1:8000/recipe/files/mak2.jpg") 
    ap4=models.Additional_photo(recipe_photo=r4, img="http://127.0.0.1:8000/recipe/files/grechka22.jpg") 
    ap5=models.Additional_photo(recipe_photo=r5, img="http://127.0.0.1:8000/recipe/files/chay2.jpg") 

    session.add_all([u1,u2,u3, i1,i2,i3,i4,i5,i6,i7, soc1,soc2,soc3,soc4,soc5, c1,c2,c3,c4,c5,c6, m1,m2,m3, r1,r2,r3,r4,r5, s1,s2,s3,s4,s5,s6,s7, ap1,ap2,ap3,ap4,ap5])
    session.commit()

