from typing import Dict
from pydantic import BaseModel, Field

class Chapter(BaseModel):
    """Pydantic model representing a Bhagavad Gita chapter."""
    number: int = Field(..., description="The chapter number (1 to 18).")
    verses_count: int = Field(..., description="Number of canonical verses in this chapter.")
    name: str = Field(..., description="Sanskrit name of the chapter.")
    translation: str = Field(..., description="English translation of the chapter name.")
    transliteration: str = Field(..., description="English transliteration of the chapter name.")
    meaning: Dict[str, str] = Field(..., description="Meaning of the chapter name (e.g. 'en', 'hi').")
    summary: Dict[str, str] = Field(..., description="Detailed chapter summary in multiple languages.")

    def __str__(self) -> str:
        from opengita.formatters.console import ConsoleFormatter
        return ConsoleFormatter.render_chapter(self)

    def __rich__(self):
        from opengita.formatters.console import ConsoleFormatter
        return ConsoleFormatter.render_rich_chapter(self)

    def __repr__(self) -> str:
        return f'Chapter(number={self.number}, name="{self.name}", translation="{self.translation}")'
