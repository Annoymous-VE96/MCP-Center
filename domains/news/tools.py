import feedparser
from feedparser.util import FeedParserDict
from urllib.parse import quote


def find_news(query:str)->FeedParserDict:
    encoded_query = quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded_query}"
    feed = feedparser.parse(rss_url)
    return feed
