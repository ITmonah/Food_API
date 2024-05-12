from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from database import get_db
import pyd

router = APIRouter(
    prefix="/system_of_calculation",
    tags=["system_of_calculation"],
)

#получение списка системы исчисления
@router.get('/', response_model=List[pyd.System_of_calculationBase])
async def get_system_of_calculations(db:Session=Depends(get_db)):
    system_of_calculations=db.query(models.System_of_calculation).all()
    return system_of_calculations

#добавление системы исчисления
@router.post('/', response_model=pyd.System_of_calculationBase)
async def create_system_of_calculations(system_of_calculation_input:pyd.System_of_calculationCreate, db:Session=Depends(get_db)):
    system_of_calculation_db=models.System_of_calculation()
    system_of_calculation_db.name=system_of_calculation_input.name

    db.add(system_of_calculation_db)
    db.commit()
    return system_of_calculation_db

#редактирование системы исчисления
@router.put('/{system_of_calculation_id}', response_model=pyd.System_of_calculationBase)
async def update_system_of_calculations(system_of_calculation_id:int, system_of_calculation_input:pyd.System_of_calculationBase, db:Session=Depends(get_db)):
    system_of_calculation_db=db.query(models.System_of_calculation).filter(models.System_of_calculation.id==system_of_calculation_id).first()
    if not system_of_calculation_db:
        raise HTTPException(status_code=404, detail="Система исчисления не найдена!")
    system_of_calculation_db.name=system_of_calculation_input.name
    db.commit()
    return system_of_calculation_db

#удаление системы исчисления
@router.delete('/{system_of_calculation_id}')
async def delete_system_of_calculation(system_of_calculation_id:int, db:Session=Depends(get_db)):
    system_of_calculation_db=db.query(models.System_of_calculation).filter(models.System_of_calculation.id==system_of_calculation_id).first()
    if not system_of_calculation_db:
        raise HTTPException(status_code=404, detail="Система исчисления не найдена!")
    db.delete(system_of_calculation_db)
    db.commit()
    return "Удаление системы исчисления прошло успешно!"