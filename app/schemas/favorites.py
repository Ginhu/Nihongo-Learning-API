from pydantic import BaseModel
from typing import List


class FavoritesResponse(BaseModel):
    kanji: List[str]
    vocabulary: List[str]


class ToggleResponse(BaseModel):
    favorited: bool
