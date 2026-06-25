import feedparser
from feedparser.util import FeedParserDict
from urllib.parse import quote
import os 
from dotenv import load_dotenv
import requests
import re
import uuid

load_dotenv()

URL_SHORTNER = os.getenv("URL_SHORTNER_API")

def find_news(query:str)->FeedParserDict:
    encoded_query = quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}"
    feed = feedparser.parse(rss_url)
    return feed



def url_shortner(longurl:str,alias:str)->str:
    alias = alias.strip().replace(" ", "_")
    alias = re.sub(r'[^a-zA-Z0-9_-]', '', alias)

    # Keep first 20 chars and add random suffix
    alias = f"{alias[:8]}_{uuid.uuid4().hex[:6]}"

    url = "https://spoo.me/api/v1/shorten"
    payload = {
    "long_url": longurl,
    "alias": alias,
    }
    headers = {
    "Authorization": URL_SHORTNER,
    "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)


    # print("Status:", response.status_code)
    # print("Response Text:", response.text)

    data = response.json()

    return data.get("short_url")
