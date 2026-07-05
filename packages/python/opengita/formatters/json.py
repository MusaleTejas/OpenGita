import json

class JSONFormatter:
    @staticmethod
    def render_verse(verse) -> str:
        return json.dumps(verse.to_dict(), indent=2, ensure_ascii=False)

    @staticmethod
    def render_chapter(chapter) -> str:
        # Pydantic v2 has model_dump() on Chapter
        return json.dumps(chapter.model_dump(), indent=2, ensure_ascii=False)
