import pytest
from opengita import Gita
from opengita.exceptions import ChapterNotFound, VerseNotFound

def test_client_verse_lookup():
    """Verify Gita.verse() retrieves the expected Verse model."""
    gita = Gita()
    
    # Valid verse
    v = gita.verse(2, 47)
    assert v is not None
    assert v.chapter == 2
    assert v.verse == 47
    assert v.id == "BG2.47"
    assert "कर्मण्येवाधिकारस्ते" in v.slok
    
    # Valid pushpika/colophon (verse 48 of chapter 1)
    colophon = gita.verse(1, 48)
    assert colophon is not None
    assert colophon.verse == 48
    assert "अर्जुनविषादयोगो नाम प्रथमोऽध्यायः" in colophon.slok

    # Non-existent chapter
    with pytest.raises(ChapterNotFound):
        gita.verse(19, 1)

    # Non-existent verse
    with pytest.raises(VerseNotFound):
        gita.verse(1, 99)

def test_client_chapter_lookup():
    """Verify Gita.chapter() retrieves the expected Chapter model."""
    gita = Gita()
    
    # Valid chapter
    ch = gita.chapter(2)
    assert ch is not None
    assert ch.number == 2
    assert ch.translation == "Sankhya Yoga"
    assert ch.verses_count == 72

    # Non-existent chapter
    with pytest.raises(ChapterNotFound):
        gita.chapter(0)
    with pytest.raises(ChapterNotFound):
        gita.chapter(19)

def test_client_statistics():
    """Verify Gita.statistics() outputs valid dataset statistics."""
    gita = Gita()
    stats = gita.statistics()
    
    assert stats.total_chapters == 18
    assert stats.total_verses == 701
    assert stats.total_files == 719
    assert stats.translators_count > 0
    assert stats.commentators_count > 0
    assert "Swami Sivananda" in stats.translators
    assert "Swami Chinmayananda" in stats.commentators
    assert len(stats.languages) >= 3
