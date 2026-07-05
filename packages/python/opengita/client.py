from typing import List
import re
from .loader import DataLoader
from .randomizer import GitaRandomizer
from .models.verse import Verse
from .models.chapter import Chapter
from .models.metadata import GitaStatistics
from .exceptions import ChapterNotFound, VerseNotFound, DatasetNotLoaded

class Gita:
    """The main user-facing SDK client for accessing Bhagavad Gita offline."""
    
    def __init__(self):
        # Initializes loader which populates the singleton cache
        self.data_loader = DataLoader()
        self.randomizer = GitaRandomizer()

    def random(self) -> Verse:
        """Fetch a random canonical Gita verse.
        
        Returns:
            Verse: A Pydantic model representing a random verse.
        """
        return self.randomizer.random_verse()

    def verse(self, chapter: int, verse: int) -> Verse:
        """Fetch a specific verse by chapter and verse number.
        
        Args:
            chapter (int): The chapter number (1 to 18).
            verse (int): The verse number.
            
        Returns:
            Verse: A Pydantic model containing the verse text, translations, and commentaries.
            
        Raises:
            ChapterNotFound: If the chapter number is out of range.
            VerseNotFound: If the verse number is out of range for the chapter.
        """
        # Validate chapter number
        ch = self.data_loader.get_chapter(chapter)
        if not ch:
            raise ChapterNotFound(f"Chapter {chapter} does not exist. Must be between 1 and 18.")
            
        # Get verse
        v = self.data_loader.get_verse(chapter, verse)
        if not v:
            raise VerseNotFound(f"Verse {verse} does not exist in Chapter {chapter}.")
            
        return v

    def chapter(self, number: int) -> Chapter:
        """Fetch details of a specific chapter.
        
        Args:
            number (int): The chapter number (1 to 18).
            
        Returns:
            Chapter: A Pydantic model containing the chapter title, summaries, and verse count.
            
        Raises:
            ChapterNotFound: If the chapter number is out of range.
        """
        ch = self.data_loader.get_chapter(number)
        if not ch:
            raise ChapterNotFound(f"Chapter {number} does not exist. Must be between 1 and 18.")
        return ch

    def statistics(self) -> GitaStatistics:
        """Fetch statistics about the SDK dataset.
        
        Returns:
            GitaStatistics: A Pydantic model containing translators, commentators, and verse counts.
            
        Raises:
            DatasetNotLoaded: If the metadata is not initialized.
        """
        meta = self.data_loader.get_metadata()
        if not meta:
            raise DatasetNotLoaded("Dataset metadata is not loaded.")
            
        return GitaStatistics(
            total_chapters=meta.total_chapters,
            total_verses=meta.total_verses,
            total_files=meta.total_files,
            languages=meta.languages,
            translators_count=len(meta.translators),
            commentators_count=len(meta.commentators),
            translators=meta.translators,
            commentators=meta.commentators,
        )

    def search(self, keyword: str) -> List[Verse]:
        """Search verses containing the keyword in Sanskrit, transliteration, translations, or commentaries.
        
        Args:
            keyword (str): The keyword to search for.
            
        Returns:
            List[Verse]: List of matching Verse objects.
        """
        keyword_clean = keyword.lower().strip()
        if not keyword_clean:
            return []
            
        words_index = self.data_loader.cache.search_index.get("words", {})
        matching_ids = set()
        
        if keyword_clean in words_index:
            matching_ids.update(words_index[keyword_clean])
        else:
            # Fallback to substring search on tokens
            for token, ids in words_index.items():
                if keyword_clean in token:
                    matching_ids.update(ids)
                    
        def parse_id(vid):
            match = re.findall(r'\d+', vid)
            return [int(x) for x in match] if match else [0, 0]
            
        sorted_ids = sorted(list(matching_ids), key=parse_id)
        
        results = []
        for vid in sorted_ids:
            parts = parse_id(vid)
            if len(parts) == 2:
                v = self.verse(parts[0], parts[1])
                if v:
                    results.append(v)
        return results
