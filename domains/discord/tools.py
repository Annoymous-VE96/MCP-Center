import httpx
from domains.discord.schemas import DiscordInput, DiscordOutput
from domains.discord.client import send_notification

def send_discord_notification(input: DiscordInput)-> DiscordOutput:
    response= send_notification(input.message)
    return DiscordOutput(
        status=response['status'],
        content=response['content']
    )
