from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from fastapi_pagination import Page, add_pagination, paginate
import threading
from youtube import start_youtube_service

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
    daemon = threading.Thread(target=start_youtube_service, daemon=True, name='Background')
    daemon.start()


@app.get("/videos", response_model=Page[schemas.Video])
async def show_videos(db: Session = Depends(get_db)):
    videos = db.query(models.Video).all()
    return paginate(videos)

@app.get("/search_videos", response_model=Page[schemas.Video])
async def search_videos(title_search: str = "", description_search: str = "", db: Session = Depends(get_db)):
    videos = db.query(models.Video).filter(models.Video.title.like("%"+title_search+"%")).filter(models.Video.description.like("%"+description_search+"%")).all()
    return paginate(videos)

add_pagination(app)