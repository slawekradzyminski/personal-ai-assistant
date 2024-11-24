import pytest
from app.chunking import is_uninformative

def test_is_uninformative():
    # given
    short_chunk = "hi"
    normal_chunk = "This is a normal length chunk of text"
    special_chars = "⌘⌘⌘⌘⌘⌘⌘⌘⌘⌘⌘⌘"
    empty_chunk = ""
    whitespace_chunk = "   "
    
    # when/then
    assert is_uninformative(short_chunk) == True
    assert is_uninformative(normal_chunk) == False
    assert is_uninformative(special_chars) == True
    assert is_uninformative(empty_chunk) == True
    assert is_uninformative(whitespace_chunk) == True 