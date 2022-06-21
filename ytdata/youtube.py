from googleapiclient.discovery import build
import datetime

api_key = "AIzaSyBDE4zeL7PRg4QVnne-PPmWjVizz545skg"
query = "cricket"
max_results = 100


def get_youtube_data(query, max_results):
    try:
        youtube = build("youtube", "v3", developerKey=api_key)
        search_word = (
            youtube.search()
            .list(q=query, part="id, snippet", maxResults=max_results)
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
    if "videoId" in result["id"]:
        video_id = result["id"]["videoId"]
    else:
        video_id = ""
    return {
        "title": result["snippet"]["title"],
        "description": result["snippet"]["description"],
        "video_id": video_id,
        "channel_id": result["snippet"]["channelId"],
        "publish_at": get_datetime(result["snippet"]["publishedAt"]),
        "thumbnail_url": result["snippet"]["thumbnails"]["medium"]["url"],
    }


youtube_data = get_youtube_data(query, 20)
for data in youtube_data:
    print(get_relevant_dict(data))