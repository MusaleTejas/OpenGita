import pytest
from pydantic import ValidationError
from opengita.models.translation import Translation, Commentary
from opengita.models.verse import Verse
from opengita.models.chapter import Chapter

def test_translation_validation():
    """Verify correct validation of Translation model fields."""
    t = Translation(author="Swami Sivananda", language="en", description="Holy battlefield")
    assert t.author == "Swami Sivananda"
    assert t.language == "en"
    assert t.description == "Holy battlefield"

    with pytest.raises(ValidationError):
        # Missing required description field
        Translation(author="Swami Sivananda", language="en")

def test_commentary_validation():
    """Verify correct validation of Commentary model fields."""
    c = Commentary(author="Swami Chinmayananda", language="hi", description="Vichar")
    assert c.author == "Swami Chinmayananda"
    assert c.language == "hi"
    assert c.description == "Vichar"

    with pytest.raises(ValidationError):
        # Missing author
        Commentary(language="sa", description="Slok comment")

def test_chapter_validation():
    """Verify correct validation of Chapter model fields."""
    ch = Chapter(
        number=1,
        verses_count=47,
        name="अर्जुनविषादयोग",
        translation="Arjuna Visada Yoga",
        transliteration="Arjun Viṣhād Yog",
        meaning={"en": "Arjuna's Dilemma", "hi": "अर्जुन विषाद योग"},
        summary={"en": "Summary text", "hi": "Saaransh"}
    )
    assert ch.number == 1
    assert ch.verses_count == 47
    assert ch.meaning["en"] == "Arjuna's Dilemma"

    with pytest.raises(ValidationError):
        # Invalid type for number
        Chapter(
            number="one",
            verses_count=47,
            name="Name",
            translation="Trans",
            transliteration="Translit",
            meaning={},
            summary={}
        )

def test_verse_validation():
    """Verify correct validation of Verse model fields."""
    v = Verse(
        id="BG1.1",
        chapter=1,
        verse=1,
        slok="धृतराष्ट्र उवाच...",
        transliteration="dhṛtarāṣṭra uvāca...",
        translations=[
            Translation(author="Author", language="en", description="Trans text")
        ],
        commentaries=[
            Commentary(author="Author", language="sa", description="Comm text")
        ]
    )
    assert v.id == "BG1.1"
    assert v.chapter == 1
    assert v.verse == 1
    assert len(v.translations) == 1
    assert len(v.commentaries) == 1

    with pytest.raises(ValidationError):
        # Invalid translations parameter
        Verse(
            id="BG1.1",
            chapter=1,
            verse=1,
            slok="Text",
            transliteration="Translit",
            translations="Invalid type"
        )
