from pydantic import BaseModel
from typing import Optional


class SettingsResponse(BaseModel):
    quiz_length: int
    romaji_visible: bool
    sound_enabled: bool
    theme: str
    language: str

    model_config = {"from_attributes": True}


class SettingsPatch(BaseModel):
    quiz_length: Optional[int] = None
    romaji_visible: Optional[bool] = None
    sound_enabled: Optional[bool] = None
    theme: Optional[str] = None
    language: Optional[str] = None
