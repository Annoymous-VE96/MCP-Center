from domains.discord.client import send_notification

message = input("Enter a Message: ")

response = send_notification(message)

print(response)