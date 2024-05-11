from sqlalchemy.orm import Session
from database import engine
import models

models.Base.metadata.drop_all(bind=engine) #пересоздание таблиц
models.Base.metadata.create_all(bind=engine) #пересоздание таблиц

with Session(bind=engine) as session:
    u1=models.User(name="Малинина", mail="recipes228@mail.ru", password="ajsdkjkf", mailing=False)
    u2=models.User(name="Хомяк", mail="recipes228@mail.ru", password="ajsdkjkf", mailing=False)
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

