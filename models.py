from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from pydantic import BaseModel
from datetime import datetime

class Feed(Base):
    __tablename__ = 'feed'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    published_at = Column(DateTime)
    thumbnail_url = Column(String)

class VideoModel(BaseModel):
    video_id: str
    title: str
    description: str
    published_at: datetime
    thumbnail_url: str