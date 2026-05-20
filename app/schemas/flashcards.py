from pydantic import BaseModel
from uuid import UUID


class FlashcardKnownResponse(BaseModel):
    card_id: str
    known: bool

    model_config = {"from_attributes": True}
