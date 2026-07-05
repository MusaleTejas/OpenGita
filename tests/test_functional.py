import opengita

def test_functional_get_methods():
    # Test random verse (just checking it returns a non-empty string reference)
    v_rand = opengita.get_random_verse()
    assert isinstance(v_rand, str)
    assert "Bhagavad Gita" in v_rand
    
    # Test specific verse
    v_spec = opengita.get_verse(2, 47)
    assert isinstance(v_spec, str)
    assert "Bhagavad Gita 2.47" in v_spec
    
    # Test chapter
    ch = opengita.get_chapter(2)
    assert isinstance(ch, str)
    assert "Chapter 2:" in ch

def test_functional_today():
    t = opengita.today()
    assert isinstance(t, str)
    assert "Bhagavad Gita" in t
    
    # Ensure it's deterministic (returns same verse on same day)
    t2 = opengita.today()
    assert t == t2

def test_functional_search():
    res = opengita.search("entitled")
    assert isinstance(res, str)
    assert "Search Results for 'entitled'" in res
    assert "Bhagavad Gita 2.47" in res

def test_functional_quote():
    q = opengita.get_random_quote()
    assert isinstance(q, str)
    assert "Bhagavad Gita" in q
