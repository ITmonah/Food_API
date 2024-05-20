from sqlalchemy.orm import Session
from database import engine
import models

models.Base.metadata.drop_all(bind=engine) #пересоздание таблиц
models.Base.metadata.create_all(bind=engine) #пересоздание таблиц

with Session(bind=engine) as session:
    #123456 и qwerty
    u1=models.User(name="Малинина", mail="recipes228@mail.ru", password="$2b$12$/2gx.pO8GYYk7yASJfH3m.rYwOgaO/GvZ6Mzvqvyq.ZdT/mnZBpRS", mailing=False, email_verify=1)
    u2=models.User(name="Хомяк", mail="recipes223@mail.ru", password="$2b$12$o3y6j3I0lS/MqDQ79AxSG.hZIBKC9JyYOUYeIaQh1lCsYeRWKzg9i", mailing=False, email_verify=1)
    i1=models.Ingredient(name="Шоколад")
    i2=models.Ingredient(name="Картошка")
    i3=models.Ingredient(name="Клубника")
    soc1=models.System_of_calculation(name="Кг")
    soc2=models.System_of_calculation(name="Л")
    c1=models.Category(name="Мясо")
    c2=models.Category(name="Рыба")
    c3=models.Category(name="Десерт")
    m1=models.Mealtime(name="Завтрак")
    m2=models.Mealtime(name="Обед")
    m3=models.Mealtime(name="Ужин")
    r1=models.Recipe(name="Чизкейк", cooking_time=3, category=c3, user=u1, mealtime=[m1,m2],ingredient=[i1,i3])
    s1=models.Step(number=1, info="Потрите сыр на тёрке", recipe=r1)
    ap1=models.Additional_photo(recipe_photo=r1)
    session.add_all([u1,u2,i1,i2,i3,soc1,soc2,c1,c2,c3,m1,m2,m3,r1,s1,ap1])
    session.commit()

