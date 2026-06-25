from domains.discord.tools import send_discord_notification
from domains.discord.schemas import DiscordInput

message = input('Enter a message : ')

print(send_discord_notification(DiscordInput(message=message)))