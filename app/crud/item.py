from sqlalchemy.orm import Session
from app.models.item import Item

def get_item(db: Session, item_id: int):
    return db.get(Item, item_id)  #  added this to fetch by primary key

def get_items(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Item).offset(skip).limit(limit).all()

def create_item(db: Session, item_create):
    db_item = Item(name=item_create.name, description=item_create.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
