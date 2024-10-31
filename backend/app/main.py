from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas, auth
from .database import engine, get_db
from .auth import get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Radio Backend API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with actual frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/auth/token", response_model=schemas.Token)
async def login_for_access_token(form_data: auth.OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = auth.create_access_token(data={"sub": user.username, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/storage/", response_model=List[schemas.DataUnitStorage])
async def list_storages(db: Session = Depends(get_db), 
                       current_user: schemas.User = Depends(get_current_user)):
    return crud.get_storages(db)

@app.post("/storage/", response_model=schemas.DataUnitStorage)
async def create_storage(storage: schemas.DataUnitStorageCreate, 
                        db: Session = Depends(get_db),
                        current_user: schemas.User = Depends(get_current_user)):
    auth.verify_editor_role(current_user)
    return crud.create_storage(db=db, storage=storage)

@app.put("/storage/{storage_id}/status")
async def update_storage_status(storage_id: int, 
                              status: bool,
                              db: Session = Depends(get_db),
                              current_user: schemas.User = Depends(get_current_user)):
    auth.verify_editor_role(current_user)
    return crud.update_storage_status(db=db, storage_id=storage_id, status=status)

@app.delete("/storage/{storage_id}")
async def delete_storage(storage_id: int,
                        db: Session = Depends(get_db),
                        current_user: schemas.User = Depends(get_current_user)):
    auth.verify_editor_role(current_user)
    return crud.delete_storage(db=db, storage_id=storage_id)

@app.post("/storage/{storage_id}/unit/")
async def create_data_unit(storage_id: int,
                          unit: schemas.DataUnitCreate,
                          db: Session = Depends(get_db),
                          current_user: schemas.User = Depends(get_current_user)):
    auth.verify_editor_role(current_user)
    return crud.create_data_unit(db=db, storage_id=storage_id, unit=unit)

@app.put("/storage/{storage_id}/units/reorder")
async def reorder_units(storage_id: int,
                       unit_ids: List[int],
                       db: Session = Depends(get_db),
                       current_user: schemas.User = Depends(get_current_user)):
    auth.verify_editor_role(current_user)
    return crud.reorder_units(db=db, storage_id=storage_id, unit_ids=unit_ids)

@app.post("/service/restart")
async def restart_service(current_user: schemas.User = Depends(get_current_user)):
    auth.verify_supervisor_role(current_user)
    # Implement service restart logic here
    return {"message": "Service restarted successfully"}