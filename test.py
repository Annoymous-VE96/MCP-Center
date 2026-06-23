# test_manual.py (put at root, delete after testing)
from domains.discord.client import send_notification

message ="Hi"
response = send_notification(message)
print(response)