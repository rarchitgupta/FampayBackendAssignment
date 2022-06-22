from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi_pagination import Page, add_pagination, paginate
from typing import List
from dotenv import load_dotenv

import models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def start_youtube_save_event():
    print("Youtube Save Started")

@app.get("/videos", response_model = List[schemas.Video])
async def show_videos(db: Session = Depends(get_db)):
    videos = db.query(models.Video).all()
    return videos


#add_pagination(app)