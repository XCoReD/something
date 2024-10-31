from sqlalchemy.orm import Session
from sqlalchemy import desc
from . import models, schemas
from typing import List
from fastapi import HTTPException, status

def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_storages(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.DataUnitStorage).offset(skip).limit(limit).all()

def create_storage(db: Session, storage: schemas.DataUnitStorageCreate):
    db_storage = models.DataUnitStorage(**storage.dict())
    db.add(db_storage)
    db.commit()
    db.refresh(db_storage)
    return db_storage

def update_storage_status(db: Session, storage_id: int, status: bool):
    storage = db.query(models.DataUnitStorage).filter(
        models.DataUnitStorage.id == storage_id
    ).first()
    if not storage:
        raise HTTPException(status_code=404, detail="Storage not found")
    storage.is_active = status
    db.commit()
    return storage

def delete_storage(db: Session, storage_id: int):
    storage = db.query(models.DataUnitStorage).filter(
        models.DataUnitStorage.id == storage_id
    ).first()
    if not storage:
        raise HTTPException(status_code=404, detail="Storage not found")
    db.delete(storage)
    db.commit()
    return {"message": "Storage deleted successfully"}

def create_data_unit(db: Session, storage_id: int, unit: schemas.DataUnitCreate):
    # Get the highest order number for the storage
    max_order = db.query(models.DataUnit).filter(
        models.DataUnit.storage_id == storage_id
    ).with_entities(models.DataUnit.order).order_by(desc(models.DataUnit.order)).first()
    
    new_order = (max_order[0] + 1) if max_order else 1
    
    db_unit = models.DataUnit(
        storage_id=storage_id,
        order=new_order,
        is_active=unit.is_active
    )
    db.add(db_unit)
    db.commit()
    
    for item in unit.content_items:
        content_item = models.ContentItem(
            data_unit_id=db_unit.id,
            **item.dict()
        )
        db.add(content_item)
    
    db.commit()
    db.refresh(db_unit)
    return db_unit

def reorder_units(db: Session, storage_id: int, unit_ids: List[int]):
    units = db.query(models.DataUnit).filter(
        models.DataUnit.storage_id == storage_id,
        models.DataUnit.id.in_(unit_ids)
    ).all()
    
    if len(units) != len(unit_ids):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid unit IDs provided"
        )
    
    # Create a mapping of id to new order
    order_map = {id: idx + 1 for idx, id in enumerate(unit_ids)}
    
    for unit in units:
        unit.order = order_map[unit.id]
    
    db.commit()
    return {"message": "Units reordered successfully"}