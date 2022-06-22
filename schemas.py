from pydantic import BaseModel

class Video(BaseModel):
    id: int
    title: str
    description: str
    published_at: str
    thumbnail_url: str

    class Config:
        orm_mode = True