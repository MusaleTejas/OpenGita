from typing import List, Optional
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

    def reference(self) -> str:
        """Returns the canonical reference of the verse (e.g. 'Bhagavad Gita 2.47')."""
        return f"Bhagavad Gita {self.chapter}.{self.verse}"

    def sanskrit(self) -> str:
        """Returns the Sanskrit text of the verse."""
        return self.slok

    def transliteration_text(self) -> str:
        """Returns the transliteration text of the verse."""
        return self.transliteration

    def translation(self, language: str = "en") -> Optional[str]:
        """Returns the translation for the specified language. Falls back to a preferred author if available."""
        matches = [t for t in self.translations if t.language.lower() == language.lower()]
        if not matches:
            return None
        # Preferred translators list
        preferred = {
            "en": ["Swami Sivananda", "A.C. Bhaktivedanta Swami Prabhupada"],
            "hi": ["Swami Ramsukhdas", "Swami Tejomayananda", "Sri Shankaracharya"]
        }
        pref_list = preferred.get(language.lower(), [])
        for p in pref_list:
            for m in matches:
                if p.lower() in m.author.lower():
                    return m.description
        return matches[0].description

    def commentary(self, language: str = "en") -> Optional[str]:
        """Returns the commentary for the specified language. Falls back to a preferred commentator if available."""
        matches = [c for c in self.commentaries if c.language.lower() == language.lower()]
        if not matches:
            return None
        # Preferred commentators list
        preferred = {
            "en": ["Swami Sivananda", "A.C. Bhaktivedanta Swami Prabhupada"],
            "hi": ["Swami Ramsukhdas", "Swami Chinmayananda"],
            "sa": ["Sri Shankaracharya", "Sri Ramanuja"]
        }
        pref_list = preferred.get(language.lower(), [])
        for p in pref_list:
            for m in matches:
                if p.lower() in m.author.lower():
                    return m.description
        return matches[0].description

    def available_languages(self) -> List[str]:
        """Returns all languages available for translations and commentaries."""
        langs = set()
        for t in self.translations:
            langs.add(t.language.lower())
        for c in self.commentaries:
            langs.add(c.language.lower())
        return sorted(list(langs))

    def available_translators(self) -> List[str]:
        """Returns the names of all translators for this verse."""
        translators = set()
        for t in self.translations:
            translators.add(t.author)
        return sorted(list(translators))

    def to_dict(self) -> dict:
        """Returns a JSON-serializable dictionary representation of the verse."""
        return self.model_dump()

    def to_json(self) -> str:
        """Returns a formatted JSON representation of the verse."""
        from opengita.formatters.json import JSONFormatter
        return JSONFormatter.render_verse(self)

    def to_markdown(self) -> str:
        """Returns a markdown representation of the verse."""
        from opengita.formatters.markdown import MarkdownFormatter
        return MarkdownFormatter.render_verse(self)

    def to_html(self) -> str:
        """Returns an HTML representation of the verse."""
        from opengita.formatters.html import HTMLFormatter
        return HTMLFormatter.render_verse(self)

    def __str__(self) -> str:
        from opengita.formatters.console import ConsoleFormatter
        return ConsoleFormatter.render_verse(self, language="en", commentary=False, transliteration=True)

    def __rich__(self):
        from opengita.formatters.console import ConsoleFormatter
        return ConsoleFormatter.render_rich_verse(self)

    def __repr__(self) -> str:
        return f'Verse(id="{self.id}", chapter={self.chapter}, verse={self.verse})'
