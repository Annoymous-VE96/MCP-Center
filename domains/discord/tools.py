import httpx
from domains.discord.schemas import DiscordInput, DiscordOutput
from domains.discord.client import send_notification

def send_discord_notification_tool(input: DiscordInput)-> DiscordOutput:
    """
    used to send any message to a already selected discord channel
    input: message that you wanna sent
    output: the message that is sent, the status
    """
    response= send_notification(input.message)
    return DiscordOutput(
        status=response['status'],
        content=response['content']
    )
