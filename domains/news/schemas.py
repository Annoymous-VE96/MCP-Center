from pydantic import BaseModel, HttpUrl
from typing import List


class NewsArticle(BaseModel):
    index: int
    title: str
    link: HttpUrl  # Use HttpUrl if all links are guaranteed valid


class NewsFeed(BaseModel):
    topic: str
    articles: List[NewsArticle]