import os
from dotenv import load_dotenv
from domains.discord.tools import send_discord_notification

load_dotenv()

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")



def send_notification(message:str)->dict:
    response= send_discord_notification(message,WEBHOOK_URL)
    return response

