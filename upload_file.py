from fastapi import FastAPI, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from database import get_db
import os

def save_file(file: UploadFile):
    if file.content_type not in ('image/jpeg','image/png'):
        raise HTTPException(400)
    #if file.size > 100000;
    # raise HTTPException(400)
    with open(f'http://127.0.0.1:8000/files/{file.filename}', 'wb') as f:
        f.write(file.file.read())
    url = str(f'files/{file.filename}')
    return url


def getim(filename):
    if os.path.exists(f'http://127.0.0.1:8000/files/{filename}'):
        return FileResponse(f'http://127.0.0.1:8000/files/{filename}')
    else: 
        return "Изображение отсутствует!"