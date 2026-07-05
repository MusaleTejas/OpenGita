import threading
from typing import Dict, Any, Optional
from .models.verse import Verse
from .models.chapter import Chapter
from .models.metadata import Metadata

class GitaCache:
    """Thread-safe singleton cache for holding Gita dataset in memory."""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(GitaCache, cls).__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        
        self.chapters: Dict[int, Chapter] = {}
        self.verses: Dict[str, Verse] = {}  # key style: "BG{chapter}.{verse}"
        self.metadata: Optional[Metadata] = None
        self.search_index: Dict[str, Any] = {}
        self._initialized = True

    def clear(self):
        """Reset the cache state (mostly useful for testing purposes)."""
        with self._lock:
            self.chapters.clear()
            self.verses.clear()
            self.metadata = None
            self.search_index.clear()
