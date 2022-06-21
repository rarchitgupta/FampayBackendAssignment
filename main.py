from fastapi import FastAPI, Depends
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from fastapi_pagination import Page, add_pagination, paginate

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_database():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/videos", response_model=Page[models.VideoModel])
async def read_all(db: Session = Depends(get_database)):
    return paginate(db.query(models.Feed).all())





add_pagination(app)