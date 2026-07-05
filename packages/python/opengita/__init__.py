import hashlib
from datetime import date

from .client import Gita
from .exceptions import (
    GitaException,
    VerseNotFound,
    ChapterNotFound,
    DatasetNotLoaded,
    LanguageNotSupported,
)

_DISPLAY_MODE = "minimal"

def set_display_mode(mode: str):
    """Set the default display mode for console outputs ('minimal', 'plain', or 'rich')."""
    global _DISPLAY_MODE
    if mode.lower() in ("plain", "minimal", "rich"):
        _DISPLAY_MODE = mode.lower()
    else:
        raise ValueError("Mode must be 'plain', 'minimal', or 'rich'")

def get_display_mode() -> str:
    """Get the current default display mode."""
    return _DISPLAY_MODE

# Functional API layer
def get_random_verse() -> str:
    """Fetch a random canonical verse, formatted for terminal display."""
    return str(Gita().random())

def get_verse(chapter: int, verse: int) -> str:
    """Fetch a specific verse, formatted for terminal display."""
    return str(Gita().verse(chapter, verse))

def get_chapter(number: int) -> str:
    """Fetch chapter information, formatted for terminal display."""
    return str(Gita().chapter(number))

def today() -> str:
    """Fetch today's verse, formatted for terminal display. 
    Determined deterministically based on today's calendar date.
    """
    gita = Gita()
    all_verses = gita.data_loader.get_all_verses()
    canonical = []
    for v in all_verses:
        ch = gita.chapter(v.chapter)
        if v.verse <= ch.verses_count:
            canonical.append(v)
    canonical = sorted(canonical, key=lambda x: (x.chapter, x.verse))
    if not canonical:
        return ""
    d_str = date.today().isoformat()
    idx = int(hashlib.md5(d_str.encode('utf-8')).hexdigest(), 16) % len(canonical)
    return str(canonical[idx])

def search(keyword: str) -> str:
    """Search for verses matching the keyword, returning a formatted preview of results."""
    gita = Gita()
    results = gita.search(keyword)
    from opengita.formatters.console import ConsoleFormatter
    return ConsoleFormatter.render_search(results, keyword)

def get_random_quote() -> str:
    """Fetch a motivational or famous quote (verse) from the Bhagavad Gita."""
    import random
    famous_verses = [
        (2, 47), (2, 20), (2, 13), (2, 62), (2, 63), 
        (4, 7), (4, 8), (6, 5), (6, 26), (9, 22), 
        (9, 26), (18, 65), (18, 66)
    ]
    ch, v = random.choice(famous_verses)
    try:
        return str(Gita().verse(ch, v))
    except Exception:
        # Fall back to random canonical verse
        return str(Gita().random())

__all__ = [
    # Layer 1: Functional API
    "get_random_verse",
    "get_verse",
    "get_chapter",
    "today",
    "search",
    "get_random_quote",
    # Layer 2: Advanced OOP API
    "Gita",
    "GitaException",
    "VerseNotFound",
    "ChapterNotFound",
    "DatasetNotLoaded",
    "LanguageNotSupported",
    "set_display_mode",
    "get_display_mode",
]
