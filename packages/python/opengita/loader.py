import json
import importlib.resources
from pathlib import Path
from typing import List, Optional

from .cache import GitaCache
from .models.verse import Verse
from .models.chapter import Chapter
from .models.metadata import Metadata
from .exceptions import DatasetNotLoaded

class DataLoader:
    """Loads and validates processed Gita JSON data into the singleton cache."""
    
    def __init__(self):
        self.cache = GitaCache()
        self.load_all()

    def load_all(self) -> None:
        """Loads and parses chapters, verses, metadata and search index into memory once."""
        if self.cache.metadata is not None:
            # Singleton cache is already populated
            return

        try:
            # 1. Attempt to load packaged data via importlib.resources
            pkg_data = importlib.resources.files("opengita") / "data"
            
            metadata_txt = (pkg_data / "metadata.json").read_text(encoding="utf-8")
            chapters_txt = (pkg_data / "chapters.json").read_text(encoding="utf-8")
            verses_txt = (pkg_data / "verses.json").read_text(encoding="utf-8")
            search_index_txt = (pkg_data / "search_index.json").read_text(encoding="utf-8")
        except Exception:
            # 2. Fall back to repository root relative path for local development
            root_dir = Path(__file__).resolve().parents[4]  # back up to C:\OpenGita
            processed_dir = root_dir / "dataset" / "processed"
            
            if not processed_dir.exists():
                raise DatasetNotLoaded(
                    "Gita dataset files could not be found. Please run the normalization script."
                )
                
            try:
                metadata_txt = (processed_dir / "metadata.json").read_text(encoding="utf-8")
                chapters_txt = (processed_dir / "chapters.json").read_text(encoding="utf-8")
                verses_txt = (processed_dir / "verses.json").read_text(encoding="utf-8")
                search_index_txt = (processed_dir / "search_index.json").read_text(encoding="utf-8")
            except FileNotFoundError as e:
                raise DatasetNotLoaded(
                    f"Processed dataset file missing: {e.filename}. Please run normalization."
                ) from e

        try:
            # Validate and populate metadata
            meta_json = json.loads(metadata_txt)
            self.cache.metadata = Metadata(**meta_json)

            # Validate and populate chapters
            ch_list = json.loads(chapters_txt)
            for ch_dict in ch_list:
                ch = Chapter(**ch_dict)
                self.cache.chapters[ch.number] = ch

            # Validate and populate verses
            v_list = json.loads(verses_txt)
            for v_dict in v_list:
                v = Verse(**v_dict)
                key = f"BG{v.chapter}.{v.verse}"
                self.cache.verses[key] = v

            # Load search index structure
            self.cache.search_index = json.loads(search_index_txt)
            
        except (json.JSONDecodeError, TypeError, ValueError) as e:
            # Reset cache in case of invalid data shape
            self.cache.clear()
            raise DatasetNotLoaded(f"Failed to parse Gita dataset files: {e}") from e

    def get_verse(self, chapter: int, verse: int) -> Optional[Verse]:
        """Lookup verse by chapter and verse number in cache."""
        key = f"BG{chapter}.{verse}"
        return self.cache.verses.get(key)

    def get_chapter(self, number: int) -> Optional[Chapter]:
        """Lookup chapter by its number in cache."""
        return self.cache.chapters.get(number)

    def get_metadata(self) -> Optional[Metadata]:
        """Get the cached metadata."""
        return self.cache.metadata

    def get_all_verses(self) -> List[Verse]:
        """Get list of all verses currently in cache."""
        return list(self.cache.verses.values())
