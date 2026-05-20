from pydantic import BaseModel


class FlashcardKnownResponse(BaseModel):
    card_id: str
    known: bool

    model_config = {"from_attributes": True}
