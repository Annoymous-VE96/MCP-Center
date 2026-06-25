from pydantic import BaseModel 

class DiscordInput(BaseModel):
    message: str

class DiscordOutput(BaseModel): 
    content: str
    status: str 