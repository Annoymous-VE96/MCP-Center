from domains.news.client import get_news_feed

topic = input("Enter a Topic: ")

response = get_news_feed(topic)

for article in response.entries:
    # for k,v in article.items():
    #     print(k)
    print("Title:",article.title)
    print("Link:",article.link)
    print("-"*50)

