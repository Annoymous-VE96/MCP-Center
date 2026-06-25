from domains.news.client import get_news_feed
from domains.news.tools import url_shortner

topic = input("Enter a Topic: ")

response = get_news_feed(topic)

for article in response.entries[:5]:
    # for k,v in article.items():
    #     print(k)
    title = article.title
    long_url = article.link
    short_url = url_shortner(long_url,title)
    print("Title:",title)
    print("Link:",short_url)
    print("-"*50)

