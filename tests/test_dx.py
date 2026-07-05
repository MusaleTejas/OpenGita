from opengita import Gita

def test_verse_helper_methods():
    gita = Gita()
    v = gita.verse(2, 47)
    
    assert v.reference() == "Bhagavad Gita 2.47"
    assert v.sanskrit() == v.slok
    assert v.transliteration_text() == v.transliteration
    
    # Translation and commentary
    assert v.translation("en") is not None
    assert v.translation("hi") is not None
    assert v.commentary("en") is not None
    
    # Available info
    langs = v.available_languages()
    assert "en" in langs
    assert "hi" in langs
    
    translators = v.available_translators()
    assert len(translators) > 0
    
    # Dict and JSON
    d = v.to_dict()
    assert isinstance(d, dict)
    assert d["id"] == "BG2.47"
    
    j = v.to_json()
    assert '"id": "BG2.47"' in j
    
    # Markdown and HTML
    md = v.to_markdown()
    assert "### 📖 Bhagavad Gita 2.47" in md
    
    html = v.to_html()
    assert 'class="opengita-verse"' in html

def test_verse_str_repr():
    gita = Gita()
    v = gita.verse(2, 47)
    
    s = str(v)
    assert "Bhagavad Gita 2.47" in s
    assert v.slok in s
    
    r = repr(v)
    assert r == 'Verse(id="BG2.47", chapter=2, verse=47)'

def test_chapter_str_repr():
    gita = Gita()
    ch = gita.chapter(2)
    
    s = str(ch)
    assert "Chapter 2:" in s
    assert ch.name in s
    
    r = repr(ch)
    assert r == f'Chapter(number=2, name="{ch.name}", translation="{ch.translation}")'
