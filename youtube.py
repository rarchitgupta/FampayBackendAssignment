from googleapiclient.discovery import build
import datetime
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from dotenv import load_dotenv

load_dotenv()

api_key = "AIzaSyBDE4zeL7PRg4QVnne-PPmWjVizz545skg"
query = "cricket"



def get_youtube_data(query, max_results):
    try:
        youtube = build("youtube", "v3", developerKey=api_key)
        search_word = (
            youtube.search()
            .list(q=query, part="id, snippet", maxResults=max_results, order="date", type="video", publishedAfter="2021-12-12T00:00:00Z")
            .execute()
        )
        results = search_word.get("items", [])
    except:
        results = {}
        raise Exception("API key quota exceeded")
    return results


def get_datetime(date_time):
    return datetime.datetime.strptime(
        date_time.split("T")[0] + " " + date_time.split("T")[1].split("Z")[0],
        "%Y-%m-%d %H:%M:%S",
    )


def get_relevant_dict(result):
    return {
        "title": result["snippet"]["title"],
        "description": result["snippet"]["description"],
        "published_at": result["snippet"]["publishedAt"],
        "thumbnail_url": result["snippet"]["thumbnails"]["medium"]["url"],
    }

def save_yt_data(query):
    db = SessionLocal()
    models.Base.metadata.create_all(bind=engine)
    youtube_data = get_youtube_data(query, 20)
    for data in youtube_data:
        yt_dict = get_relevant_dict(data)
        yt_record = models.Video(
            title = yt_dict["title"],
            description = yt_dict["description"],
            published_at =  yt_dict["published_at"],
            thumbnail_url =  yt_dict["thumbnail_url"]
        )
        db.add(yt_record)
    db.commit()

save_yt_data("cricket")