import os
from dotenv import load_dotenv

import httpx

load_dotenv()

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")



def send_notification(message:str)->dict:
    webhook_url = WEBHOOK_URL
    payload = {"content":message}
    response = httpx.post(webhook_url,json=payload)
    return {'status': 'sent', 'content': message}


