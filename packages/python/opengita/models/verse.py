from typing import List
from pydantic import BaseModel, Field
from .translation import Translation, Commentary

class Verse(BaseModel):
    """Pydantic model representing a complete Bhagavad Gita verse (slok)."""
    id: str = Field(..., description="Unique verse identifier (e.g., 'BG1.1').")
    chapter: int = Field(..., description="The chapter number.")
    verse: int = Field(..., description="The verse number within the chapter.")
    slok: str = Field(..., description="Original Sanskrit verse text.")
    transliteration: str = Field(..., description="English transliteration of the Sanskrit verse.")
    translations: List[Translation] = Field(default_factory=list, description="List of translations for this verse.")
    commentaries: List[Commentary] = Field(default_factory=list, description="List of commentaries for this verse.")
