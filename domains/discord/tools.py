import httpx


def send_discord_notification(message: str, url)-> dict:
    webhook_url = url
    payload = {"content":message}
    response = httpx.post(webhook_url,json=payload)
    response.raise_for_status
    return {'status':'sent','content':message}

