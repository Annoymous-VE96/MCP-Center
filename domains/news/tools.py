from feedparser.util import FeedParserDict
from domains.news.client import find_news

def get_news_feed_tool(query:str)->FeedParserDict:
    feed = find_news(query)
    return feed


