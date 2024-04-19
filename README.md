Для установки модулей

'pip install -r requirements.txt'

Для запуска сервера

'py -m uvicorn main:app --reload'

Для создания таблиц и посева

'py seed.py'


За что отвечают файлы
1. database.py - подключение к БД
2. models.py - таблицы БД с описанием связей
3. seed.py - посев (стартовые данные)
4. pyd (папка) - pydantic модели для валидации