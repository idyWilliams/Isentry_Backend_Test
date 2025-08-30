from fastapi import FastAPI
from app.db.database import Base, engine
from app.routers import item

app = FastAPI(title="CRUD Intern Test")

Base.metadata.create_all(bind=engine)

app.include_router(item.router)

