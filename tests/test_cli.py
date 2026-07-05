import sys
from unittest.mock import patch
import pytest
from opengita.cli import main

def test_cli_help(capsys):
    with patch.object(sys, 'argv', ['opengita']):
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 0
        captured = capsys.readouterr()
        assert "Usage:" in captured.out

def test_cli_random(capsys):
    with patch.object(sys, 'argv', ['opengita', 'random']):
        main()
        captured = capsys.readouterr()
        assert "Bhagavad Gita" in captured.out

def test_cli_today(capsys):
    with patch.object(sys, 'argv', ['opengita', 'today']):
        main()
        captured = capsys.readouterr()
        assert "Bhagavad Gita" in captured.out

def test_cli_verse(capsys):
    with patch.object(sys, 'argv', ['opengita', 'verse', '2', '47']):
        main()
        captured = capsys.readouterr()
        assert "Bhagavad Gita 2.47" in captured.out

def test_cli_chapter(capsys):
    with patch.object(sys, 'argv', ['opengita', 'chapter', '2']):
        main()
        captured = capsys.readouterr()
        assert "Chapter 2:" in captured.out

def test_cli_search(capsys):
    with patch.object(sys, 'argv', ['opengita', 'search', 'karma']):
        main()
        captured = capsys.readouterr()
        assert "Search Results for 'karma'" in captured.out

def test_cli_colon_format(capsys):
    with patch.object(sys, 'argv', ['opengita', '2:47']):
        main()
        captured = capsys.readouterr()
        assert "Bhagavad Gita 2.47" in captured.out
