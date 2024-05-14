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

Работа с токенами:
Создаём эти ключи в папку certs
1. Генерируем приватный ключ размера 2048 и даём ему название "jwt-private.pem"
openssl genrsa -out jwt-private.pem 2048
2. На основе приватного ключа создаём публичный ключ
openssl rsa -in jwt-private.pem -outform PEM -pubout -out jwt-public.pem

*скачивание openssl: https://linuxhint.com/install-openssl-windows/ 
**указание пути, в случае ошибки: https://www.youtube.com/watch?v=INFZyVKIO90&t=67s 

