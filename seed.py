from sqlalchemy.orm import Session
from database import engine
import models

models.Base.metadata.drop_all(bind=engine) #пересоздание таблиц
models.Base.metadata.create_all(bind=engine) #пересоздание таблиц

with Session(bind=engine) as session:
    #123456 и qwerty
    u1=models.User(name="Малинина", mail="recipes228@mail.ru",img_avatar="recipe/files/food.png", password="$2b$12$/2gx.pO8GYYk7yASJfH3m.rYwOgaO/GvZ6Mzvqvyq.ZdT/mnZBpRS", mailing=False, email_verify=1) #пользователи
    u2=models.User(name="Хомяк", mail="recipes223@mail.ru",img_avatar="recipe/files/food.png", password="$2b$12$o3y6j3I0lS/MqDQ79AxSG.hZIBKC9JyYOUYeIaQh1lCsYeRWKzg9i", mailing=False, email_verify=1)
    u3=models.User(name="edok228", mail="admin@mail.ru",img_avatar="recipe/files/food.png", password="$2b$12$3/w7zRoYtYe4344FtJtlRuKDkfLAiZd3XqZaHaxn1zJ/DFcG/Brs6", mailing=True, email_verify=1)
    u4=models.User(name="Любимка", mail="lovelove@mail.ru",img_avatar="recipe/files/food.png", password="$2b$12$3/w7zRoYtYe4344FtJtlRuKDkfLAiZd3XqZaHaxn1zJ/DFcG/Brs6", mailing=True, email_verify=1)
    u5=models.User(name="Обжоркин", mail="objorkin@mail.ru",img_avatar="recipe/files/food.png", password="$2b$12$3/w7zRoYtYe4344FtJtlRuKDkfLAiZd3XqZaHaxn1zJ/DFcG/Brs6", mailing=True, email_verify=1)
    
    c1=models.Category(name="Десерт") #категории
    c2=models.Category(name="Мясо")
    c3=models.Category(name="Суп")
    c4=models.Category(name="Рыба")
    c5=models.Category(name="Напиток")
    c6=models.Category(name="Основное")

    m1=models.Mealtime(name="Завтрак") #время приёма пищи
    m2=models.Mealtime(name="Обед")
    m3=models.Mealtime(name="Ужин")

    i1=models.Ingredient(name="Пшеничная мука") #ингредиенты
    i2=models.Ingredient(name="Вода") #пицца
    i3=models.Ingredient(name="Сухие дрожжи")
    i4=models.Ingredient(name="Растительное масло")
    i5=models.Ingredient(name="Сахар")
    i6=models.Ingredient(name="Соль")
    i7=models.Ingredient(name="Помидоры")
    i8=models.Ingredient(name="Майонез") 
    i9=models.Ingredient(name="Кетчуп")
    i10=models.Ingredient(name="Чеснок")
    i11=models.Ingredient(name="Приправы")
    i12=models.Ingredient(name="Сыр Моцарелла")
    i13=models.Ingredient(name="Сырокопчёнаая колбаса")
    i14=models.Ingredient(name="Оливковое масло")
    i15=models.Ingredient(name="Шоколад") #клубника в шоколаде
    i16=models.Ingredient(name="Клубника")
    i17=models.Ingredient(name="Макароны") #макароны с сыром
    i18=models.Ingredient(name="Гречневая крупа") #гречка с молоком
    i19=models.Ingredient(name="Молоко")
    i20=models.Ingredient(name="Сливочное масло")
    i21=models.Ingredient(name="Малина") #чай с малиной
    i22=models.Ingredient(name="Чёрный чай")
    i23=models.Ingredient(name="Лайм")
    i24=models.Ingredient(name="Мята")
    i25=models.Ingredient(name="Сметана") #манник
    i26=models.Ingredient(name="Манка")
    i27=models.Ingredient(name="Яйцо")
    i28=models.Ingredient(name="Горошек") #добавочные
    i29=models.Ingredient(name="Огурцы")
    i30=models.Ingredient(name="Лосось")
    i31=models.Ingredient(name="Сгущёнка")
    i32=models.Ingredient(name="Зелёный чай")
    i33=models.Ingredient(name="Курица")
    i34=models.Ingredient(name="Телятина")
    i35=models.Ingredient(name="Баранина")
    i36=models.Ingredient(name="Яблоко")
    i37=models.Ingredient(name="Банан")
    i38=models.Ingredient(name="Груша")
    i39=models.Ingredient(name="Печенье")
    i40=models.Ingredient(name="Картофель")

    soc1=models.System_of_calculation(name="Кг") #система исчисления
    soc2=models.System_of_calculation(name="Г")
    soc3=models.System_of_calculation(name="Л")
    soc4=models.System_of_calculation(name="Мл")
    soc5=models.System_of_calculation(name="Шт")
    soc6=models.System_of_calculation(name="Стол. л.")
    soc7=models.System_of_calculation(name="Чайн. л.")

    r1=models.Recipe(name="Пицца", face_img="recipe/files/pizza.jpg", cooking_time=120, category=c6, user=u1, mealtime=[m2,m3], published=False) #рецепты
    r2=models.Recipe(name="Клубника в шоколаде", face_img="recipe/files/choko.jpg", cooking_time=30, category=c1, user=u1, mealtime=[m1],published=True) 
    r3=models.Recipe(name="Макароны с сыром", face_img="recipe/files/mak.jpg", cooking_time=20, category=c6, user=u2, mealtime=[m2,m3],published=True) 
    r4=models.Recipe(name="Гречка с молоком", face_img="recipe/files/grechka.jpg", cooking_time=60, category=c6, user=u1, mealtime=[m1,m2,m3],published=False) 
    r5=models.Recipe(name="Чай с малиной", face_img="recipe/files/chay.jpg", cooking_time=15, category=c5, user=u2, mealtime=[m1,m2,m3],published=True) 
    r6=models.Recipe(name="Манник", face_img="recipe/files/mannik.jpg", cooking_time=100, category=c1, user=u4, mealtime=[m1,m2,m3],published=True) 

    #пицца
    s1=models.Step(number=1, info="В тёплой воде, нагретой до 37-40°С, растворите сахар. А затем всыпьте дрожжи и оставьте на 15 минут до появления пышной шапочки. Если шапочки так и не появилось, то либо дрожжи испорчены, либо перегрели воду и тесто не поднимется. Нужно замешивать заново.", recipe=r1) #шаги
    s2=models.Step(number=2, info="В миску просейте муку. Всыпьте соль. Перемешайте все и сделайте в центре муки углубление. Влейте в него активированные дрожжи и оливковое масло.", recipe=r1) 
    s3=models.Step(number=3, info="Замесите упругое однородное тесто. Замешивать нужно около 7-10 минут, пока тесто не начнет отлипать от рук. При необходимости можно добавить ещё немного оливкового масла. Накройте миску полотенцем и оставьте тесто на 45 минут в тепле для подъёма.", recipe=r1)
    s4=models.Step(number=4, info="Пока поднимается тесто, приготовьте соус. В чаше блендера соедините помидоры, кетчуп, дольки чеснока, приправы и майонез. Взбейте все до однородности.", recipe=r1)
    s5=models.Step(number=5, info="В сковороде на среднем огне разогрейте растительное масло. Вылейте взбитую томатную смесь. Тушите, помешивая, около 5 минут до испарения жидкости и густоты.", recipe=r1)
    s6=models.Step(number=6, info="Готовый соус снимите с огня и охладите.", recipe=r1)
    s7=models.Step(number=7, info="Теперь приготовьте начинку. Колбасу нарежьте тонкими кружочками. Моцареллу натрите на крупной терке.", recipe=r1)
    s8=models.Step(number=8, info="Тесто обомните и раскатайте в тонкую круглую лепешку диаметром около 30 см.", recipe=r1)
    s9=models.Step(number=9, info="Перенесите лепёшку на застелённый пергаментом противень. Это нужно делать сразу, до того, как выложите начинку.", recipe=r1)
    s10=models.Step(number=10, info="Обильно смажьте тесто пряным томатным соусом. Сверху посыпьте тертым сыром. Поверх равномерно распределите кружочки пепперони.", recipe=r1)
    s11=models.Step(number=11, info="Выпекайте пиццу в разогретой до 250°С духовке 8-10 минут. Точное время зависит от вашей духовки. Если есть возможность включить режим 'верх+низ+конвекция', используйте его.", recipe=r1)
    #клубника в шоколаде
    s12=models.Step(number=1, info="Клубнику промойте под проточной холодной водой прямо в дуршлаге. Оставьте ягоды в нём же, чтобы стекла лишняя жидкость. Хвостики не отрывайте, за них будет удобно держать десерт при поедании.", recipe=r2)
    s13=models.Step(number=2, info="Затем разложите клубнику сохнуть на бумажное полотенце. Дополнительно оботрите каждую ягоду — лишняя влага помешает шоколаду покрыть клубнику равномерно. Разложите сухие ягоды на тарелку в один слой и уберите минут на 10-15 в морозилку — на охлажденных ягодах шоколадная глазурь застынет быстрее и не стечёт.", recipe=r2)
    s14=models.Step(number=3, info="Поставьте шоколад в микроволновку на максимальную мощность, время установите 20 секунд (или больше, в зависимости от модели и мощности).", recipe=r2)
    s15=models.Step(number=4, info="Перемешайте шоколад до однородности. Влейте в него растительное масло — оно сделает глазурь более жидкой и удобной в работе.", recipe=r2)
    s16=models.Step(number=5, info="Достаньте из морозилки клубнику. Насадите ягоду на деревянную шпажку. Обмакните ее в растопленный шоколад, кончик с хвостиком можно оставить голеньким. Выкладывайте глазированные ягоды на доску, накрытую пергаментом.", recipe=r2)
    s17=models.Step(number=6, info="Украсьте ягоды полосочками из шоколада контрастного цвета. Вы также можете посыпать их дроблёными орехами, кокосовой стружкой, сублимированными ягодами, кондитерской посыпкой. Уберите доску с клубникой в холодильник для полной стабилизации глазури (хватит 10 минут).", recipe=r2)
    #макароны с сыром
    s18=models.Step(number=1, info="Отварите макароны в кастрюле согласно инструкции на упаковке, обязательно хорошо посолите воду.", recipe=r3)
    s19=models.Step(number=2, info="Натрите на терке весь сыр в нагретую сковороду и добавьте к нему ложку приправ. Хорошо мешайте лопаткой до тех пор, пока весь сыр не расплавится.", recipe=r3)
    s20=models.Step(number=3, info="Отварные макароны выложите в приготовленный сыр. Перемешайте", recipe=r3)
    #гречка с молоком
    s21=models.Step(number=1, info="Гречку залить кипятком, посолить. Довести до кипения. Убавить огонь до минимального, накрыть крышкой.", recipe=r4)
    s22=models.Step(number=2, info="Кашу варить до готовности, около 25-30 минут.", recipe=r4)
    s23=models.Step(number=3, info="Готовую кашу разложить в тарелки и залить молоком. Добавить в гречневую кашу с молоком кусочек масла.", recipe=r4)
    #чай с малиной
    s24=models.Step(number=1, info="Заварить чёрный чай, охладить. И перелить в кувшин.", recipe=r5)
    s25=models.Step(number=2, info="Малину хорошо промыть и высыпать в охлаждённый чай, добавить воду.", recipe=r5)
    s26=models.Step(number=3, info="Лайм нарежьте кружочками и добавьте в кувшин, по вкусу положите сахар.", recipe=r5)
    s27=models.Step(number=4, info="Украсьте освежающий напиток листиками мяты.", recipe=r5)
    #манник
    s28=models.Step(number=1, info="В миске соедините сметану комнатной температуры и манную крупу. Все хорошенько перемешайте до однородности и оставьте массу на 30 минут, чтобы крупа разбухла. Очень важно, чтобы манка как следует разбухла. Ведь от этого зависит, насколько мягким и нежным получится пирог.", recipe=r6)
    s29=models.Step(number=2, info="В другой миске яйца соедините с сахаром и щепоткой соли. Всё взбейте миксером до пышности примерно 2 минуты. Должна получиться пышная масса с множеством мелких воздушных пузырьков. От того, как вы взобьете яйца, зависит воздушность готовой выпечки.", recipe=r6)
    s30=models.Step(number=3, info="Добавьте в яичную смесь разбухшую в сметане манку и снова взбейте все миксером. В массе не должно остаться никаких комочков.", recipe=r6)
    s31=models.Step(number=4, info="Всыпьте просеянную муку и снова перемешайте тесто до однородности миксером.", recipe=r6)
    s32=models.Step(number=5, info="Вылейте готовое тесто в застеленную пергаментом и смазанную растительным маслом форму для выпекания (Ø 18-20 см). Поставьте манник в разогретую до 180°С духовку примерно на 40-50 минут.", recipe=r6)

    ap1=models.Additional_photo(recipe_photo=r1, img="recipe/files/pizza2.jpg") #дополнительные фото
    ap2=models.Additional_photo(recipe_photo=r1, img="recipe/files/pizza3.jpg") 
    ap3=models.Additional_photo(recipe_photo=r2, img="recipe/files/choko2.jpg") 
    ap4=models.Additional_photo(recipe_photo=r2, img="recipe/files/choko3.jpg")
    ap5=models.Additional_photo(recipe_photo=r2, img="recipe/files/choko4.jpg")
    ap6=models.Additional_photo(recipe_photo=r3, img="recipe/files/mak2.jpg") 
    ap7=models.Additional_photo(recipe_photo=r4, img="recipe/files/grechka2.jpg")
    ap8=models.Additional_photo(recipe_photo=r5, img="recipe/files/chay2.jpg")
    ap9=models.Additional_photo(recipe_photo=r6, img="recipe/files/mannik2.jpg")
    ap10=models.Additional_photo(recipe_photo=r6, img="recipe/files/mannik3.jpg")
    ap11=models.Additional_photo(recipe_photo=r6, img="recipe/files/mannik4.jpg")

    #пицца
    count1=models.Count(recipe=r1, ingredient=i1, count=250, system_of_calc=soc2)
    count2=models.Count(recipe=r1, ingredient=i2, count=120, system_of_calc=soc4)
    count3=models.Count(recipe=r1, ingredient=i3, count=10, system_of_calc=soc2)
    count4=models.Count(recipe=r1, ingredient=i4, count=1, system_of_calc=soc6)
    count5=models.Count(recipe=r1, ingredient=i5, count=1, system_of_calc=soc2)
    count6=models.Count(recipe=r1, ingredient=i6, count=1, system_of_calc=soc2)
    count7=models.Count(recipe=r1, ingredient=i7, count=2, system_of_calc=soc5)
    count8=models.Count(recipe=r1, ingredient=i14, count=1, system_of_calc=soc6)
    count9=models.Count(recipe=r1, ingredient=i9, count=1, system_of_calc=soc6)
    count10=models.Count(recipe=r1, ingredient=i8, count=1, system_of_calc=soc6)
    count11=models.Count(recipe=r1, ingredient=i10, count=2, system_of_calc=soc5)
    count12=models.Count(recipe=r1, ingredient=i11, count=1, system_of_calc=soc6)
    count13=models.Count(recipe=r1, ingredient=i12, count=120, system_of_calc=soc2)
    count14=models.Count(recipe=r1, ingredient=i13, count=100, system_of_calc=soc2)
    #клубника в шоколаде
    count15=models.Count(recipe=r2, ingredient=i15, count=800, system_of_calc=soc2)
    count16=models.Count(recipe=r2, ingredient=i16, count=90, system_of_calc=soc2)
    count17=models.Count(recipe=r2, ingredient=i4, count=2, system_of_calc=soc7)
    #макароны с сыром  
    count17=models.Count(recipe=r3, ingredient=i17, count=300, system_of_calc=soc2)
    count18=models.Count(recipe=r3, ingredient=i12, count=200, system_of_calc=soc2)
    count19=models.Count(recipe=r3, ingredient=i11, count=1, system_of_calc=soc7)
    count20=models.Count(recipe=r3, ingredient=i6, count=1, system_of_calc=soc7)
    #гречка с молоком
    count21=models.Count(recipe=r4, ingredient=i6, count=1, system_of_calc=soc7)
    count22=models.Count(recipe=r4, ingredient=i18, count=200, system_of_calc=soc2)
    count23=models.Count(recipe=r4, ingredient=i19, count=1, system_of_calc=soc3)
    count24=models.Count(recipe=r4, ingredient=i20, count=40, system_of_calc=soc2)
    #чай с малиной
    count25=models.Count(recipe=r5, ingredient=i21, count=100, system_of_calc=soc2)
    count26=models.Count(recipe=r5, ingredient=i22, count=5, system_of_calc=soc5)
    count27=models.Count(recipe=r5, ingredient=i23, count=1, system_of_calc=soc5)
    count28=models.Count(recipe=r5, ingredient=i24, count=2, system_of_calc=soc5)
    count29=models.Count(recipe=r5, ingredient=i5, count=1, system_of_calc=soc6)
    count30=models.Count(recipe=r5, ingredient=i2, count=700, system_of_calc=soc4)
    #манник
    count31=models.Count(recipe=r6, ingredient=i25, count=250, system_of_calc=soc2)
    count32=models.Count(recipe=r6, ingredient=i26, count=200, system_of_calc=soc2)
    count33=models.Count(recipe=r6, ingredient=i27, count=3, system_of_calc=soc5)
    count34=models.Count(recipe=r6, ingredient=i5, count=200, system_of_calc=soc2)
    count35=models.Count(recipe=r6, ingredient=i1, count=150, system_of_calc=soc2)
    count36=models.Count(recipe=r6, ingredient=i6, count=1, system_of_calc=soc7)

    score1=models.Score(user=u1, recipe=r2, like=True, dizlike=False) #баллы
    score2=models.Score(user=u2, recipe=r2, like=True, dizlike=False)
    score3=models.Score(user=u2, recipe=r3, like=False, dizlike=True)
    score4=models.Score(user=u5, recipe=r3, like=True, dizlike=False)
    score5=models.Score(user=u5, recipe=r5, like=False, dizlike=True)
    score6=models.Score(user=u5, recipe=r6, like=True, dizlike=False)
    score7=models.Score(user=u1, recipe=r6, like=True, dizlike=False)
    score8=models.Score(user=u4, recipe=r5, like=True, dizlike=False)

    session.add_all([u1,u2,u3,u4,u5,
                    c1,c2,c3,c4,c5,c6,
                    m1,m2,m3,
                    i1,i2,i3,i4,i5,i6,i7,i8,i9,i10,i11,i12,i13,i14,i15,i16,i17,i18,i19,i20,i21,i22,i23,i24,i25,i26,i27,i28,i29,i30,i31,i32,i33,i34,i35,i36,i37,i38,i39,i40,
                    soc1,soc2,soc3,soc4,soc5,soc6,soc7,
                    r1,r2,r3,r4,r5,r6,
                    s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,s16,s17,s18,s19,s20,s21,s22,s23,s24,s25,s26,s27,s28,s29,s30,s31,s32,
                    ap1,ap2,ap3,ap4,ap5,ap6,ap7,ap8,ap9,ap10,ap11, 
                    count1,count2,count3,count4,count5,count6,count7,count8,count9,count10,
                    count11,count12,count13,count14,count15,count16,count17,count18,count19,count20,
                    count21,count22,count23,count24,count25,count26,count27,count28,count29,count30,
                    count31,count32,count33,count34,count35,count36,
                    score1,score2,score3,score4,score5,score6,score7,score8])
    session.commit()

