from opengita import Gita
from opengita.models.verse import Verse

def test_random_verse_returns_valid_model():
    """Verify Gita.random() returns a valid Verse object."""
    gita = Gita()
    r = gita.random()
    assert isinstance(r, Verse)
    assert r.chapter >= 1 and r.chapter <= 18

def test_random_verse_excludes_pushpikas():
    """Verify that random verse selection does not return colophon/pushpika verses."""
    gita = Gita()
    
    # Run random selection multiple times and verify verse <= verses_count of its chapter
    for _ in range(100):
        r = gita.random()
        ch = gita.chapter(r.chapter)
        assert r.verse <= ch.verses_count, f"Random verse selected a pushpika: {r.id}"

def test_random_verse_distribution():
    """Verify random returns different verses when called multiple times."""
    gita = Gita()
    seen_ids = set()
    for _ in range(10):
        seen_ids.add(gita.random().id)
    # With 701 canonical verses, selecting 10 random verses should result in multiple unique verses
    assert len(seen_ids) > 1
