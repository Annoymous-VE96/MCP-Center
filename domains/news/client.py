from feedparser.util import FeedParserDict
from domains.news.tools import find_news

def get_news_feed(query:str)->FeedParserDict:
    feed = find_news(query)
    return feed


