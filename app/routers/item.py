from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.item import ItemCreate, ItemSchema
from app.crud import item
from app.db.database import SessionLocal

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/items/", response_model=ItemSchema)
def create_item(item_create: ItemCreate, db: Session = Depends(get_db)):
    return item.create_item(db, item_create)

@router.get("/items/", response_model=list[ItemSchema])
def read_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return item.get_items(db, skip=skip, limit=limit)

