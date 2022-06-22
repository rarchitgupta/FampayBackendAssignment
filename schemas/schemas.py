from pydantic import BaseModel

# pydantic model for interacting with FastAPI
class Video(BaseModel):
    id: int
    title: str
    description: str
    published_at: str
    thumbnail_url: str

    class Config:
        orm_mode = True