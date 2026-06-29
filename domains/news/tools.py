from feedparser.util import FeedParserDict
from domains.news.client import find_news
from shared.db import log_activity


def get_news_feed_tool(query:str)->FeedParserDict:
    """
    gets news based on the user query
    input: the query string
    output: a dictionary of key value pairs containing the link, body, heading etc. 
    """
    log_activity('news', 'got news feed')
    feed = find_news(query)
    return feed


