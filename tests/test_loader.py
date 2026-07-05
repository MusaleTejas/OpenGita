import pytest
from unittest import mock
from opengita.loader import DataLoader
from opengita.cache import GitaCache
from opengita.exceptions import DatasetNotLoaded

def test_data_loader_initialization():
    """Verify data loader correctly loads the dataset and populates the cache."""
    loader = DataLoader()
    assert loader.cache.metadata is not None
    assert loader.cache.metadata.total_chapters == 18
    assert loader.cache.metadata.total_verses == 701
    assert loader.cache.metadata.total_files == 719

    # Verify lookups from cache
    ch = loader.get_chapter(1)
    assert ch is not None
    assert ch.number == 1
    assert ch.verses_count == 47

    verse = loader.get_verse(1, 1)
    assert verse is not None
    assert verse.chapter == 1
    assert verse.verse == 1
    assert verse.id == "BG1.1"

def test_singleton_cache():
    """Verify that multiple DataLoader instances share the same singleton GitaCache."""
    loader1 = DataLoader()
    loader2 = DataLoader()
    assert loader1.cache is loader2.cache
    
    # Assert modifications to one affect the other
    original_meta = loader1.cache.metadata
    loader1.cache.metadata = None
    assert loader2.cache.metadata is None
    
    # Re-load to restore cache state
    loader1.load_all()
    assert loader1.cache.metadata == original_meta

def test_dataset_not_found_raises_exception():
    """Verify that DataLoader raises DatasetNotLoaded when processed files are missing."""
    cache = GitaCache()
    cache.clear()
    
    # Mock importlib.resources to fail and use a non-existent fallback directory
    with mock.patch("importlib.resources.files", side_effect=Exception("No resource")), \
         mock.patch("pathlib.Path.exists", return_value=False):
        with pytest.raises(DatasetNotLoaded):
            DataLoader()
            
    # Clean up and reload dataset to fix cache for other tests
    DataLoader()
