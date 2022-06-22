import time
from googleapiclient.discovery import build
import models.models as models
from database import engine, SessionLocal
from settings import query, api_keys


available_api_keys = api_keys

def get_youtube_data(query, max_results):
    """
    Takes in the query string and max_results as parameters and returns data
    fetched from the youtube API
    """
    if len(available_api_keys):
        api_key = available_api_keys[0]
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
        available_api_keys.pop(0)
        if len(available_api_keys) == 0:
            raise Exception("API key quota exceeded")
        else:
            get_youtube_data(query, max_results)
    return results


def get_relevant_dict(result):
    """
    Takes each result from the youtube_data passed and converts it into a
    python dictionary with relevant fields to be stored in the database
    """
    return {
        "title": result["snippet"]["title"],
        "description": result["snippet"]["description"],
        "published_at": result["snippet"]["publishedAt"],
        "thumbnail_url": result["snippet"]["thumbnails"]["medium"]["url"],
    }

def save_yt_data():
    """
    Function that retrieves the relevant YT data dictionary
    and writes it to SQL database
    """
    db = SessionLocal()
    models.Base.metadata.create_all(bind=engine)
    youtube_data = get_youtube_data(query, 5)
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

def start_youtube_service():
    """
    Periodically running YT function
    """
    while True:
        save_yt_data()
        time.sleep(30)