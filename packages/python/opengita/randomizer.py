import random
from typing import List
from .models.verse import Verse
from .cache import GitaCache

class GitaRandomizer:
    """O(1) random verse selection, ignoring colophon/pushpika items."""
    
    def __init__(self):
        self.cache = GitaCache()
        self._canonical_verses: List[Verse] = []
        self._populate_canonical_verses()

    def _populate_canonical_verses(self) -> None:
        """Filter out colophon/pushpika entries for random selection."""
        for v in self.cache.verses.values():
            ch = self.cache.chapters.get(v.chapter)
            if ch and v.verse <= ch.verses_count:
                self._canonical_verses.append(v)

    def random_verse(self) -> Verse:
        """Select a random canonical verse in O(1) time."""
        if not self._canonical_verses:
            # Fallback in case of empty list, select from all loaded verses
            if not self.cache.verses:
                raise ValueError("No verses available in cache.")
            return random.choice(list(self.cache.verses.values()))
        return random.choice(self._canonical_verses)
