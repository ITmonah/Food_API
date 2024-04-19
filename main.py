from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models
import pyd
from typing import List

app = FastAPI()

#получение списка аниме
@app.get('/animes', response_model=List[pyd.AnimeScheme])
async def get_animes(db:Session=Depends(get_db)):
    animes=db.query(models.Anime).all()
    return animes

