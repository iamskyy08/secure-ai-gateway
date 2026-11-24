from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=16000)
    model: str | None = None

class ChatResponse(BaseModel):
    response: str
    model: str
    request_id: str
