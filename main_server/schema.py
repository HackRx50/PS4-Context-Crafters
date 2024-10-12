from pydantic import BaseModel

class Chat(BaseModel):
    query: str
    document_id: str | None = None
    agent_id: str | None = None

class ChatResponse(BaseModel):
    bot_message: str
    reference: str | None = None