from fastapi import FastAPI, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db
import os
import random, string

def save_file(file: UploadFile):
    if file.content_type not in ('image/jpeg','image/png'):
        raise HTTPException(400)
    #if file.size > 100000;
    # raise HTTPException(400)
    file_path = f'files/{file.filename}'
    if not os.path.exists(file_path): #если файла с таким названием нет
        with open(f'files/{file.filename}', 'wb') as f:
            f.write(file.file.read())
        url = str(f'recipe/files/{file.filename}')
        return url
    else:
        letters = string.ascii_lowercase+string.digits
        stroka = ''.join(random.choice(letters) for i in range(10))
        with open(f'files/{stroka}_{file.filename}', 'wb') as f:
            f.write(file.file.read())
        url = str(f'recipe/files/{stroka}_{file.filename}')
        return url


def getim(filename):
    if os.path.exists(f'recipe/files/{filename}'):
        return FileResponse(f'recipe/files/{filename}')
    else: 
        return "Изображение отсутствует!"