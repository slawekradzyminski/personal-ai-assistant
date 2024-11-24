import pytest
from app.chunking import (
    create_chunks,
    _process_paragraph,
    _split_into_sentences,
    _normalize_sentence,
    _process_sentence,
    _exceeds_memory_limit,
    _is_uninformative,
)
from app.config import tokenizer


def test_create_chunks():
    given_text = "First paragraph.\n\nSecond paragraph.\n\nThird paragraph."

    when_chunks = create_chunks(text=given_text, chunk_sz=100)
    for chunk in when_chunks:
        print(chunk)
        print("\n")

    then_expected = ["First paragraph. Second paragraph. Third paragraph."]
    assert when_chunks == then_expected


def test_create_chunks_memory_limit():
    given_text = "x " * 1000

    with pytest.raises(
        ValueError, match="Processing is aborted due to high anticipated costs."
    ):
        create_chunks(text=given_text, chunk_sz=10, max_memory=5)


def test_process_paragraph():
    given_paragraph = "First sentence. Second sentence."
    given_current = []
    given_length = 0

    when_current, when_length, when_chunks = _process_paragraph(
        given_paragraph, given_current, given_length, chunk_sz=100
    )

    then_expected_chunks = []
    assert when_chunks == then_expected_chunks
    assert "First sentence." in when_current
    assert "Second sentence." in when_current


def test_split_into_sentences():
    given_paragraph = "First sentence.\nSecond sentence. Third sentence"

    when_result = _split_into_sentences(given_paragraph)

    then_expected = ["First sentence.", "Second sentence.", "Third sentence."]
    assert when_result == then_expected


def test_normalize_sentence():
    given_sentence = "Hello world"

    when_result = _normalize_sentence(given_sentence)

    then_expected = "Hello world."
    assert when_result == then_expected


def test_process_sentence():
    given_sentence = "Test sentence."
    given_current = []
    given_length = 0

    when_current, when_length, when_chunk = _process_sentence(
        given_sentence, given_current, given_length, chunk_sz=100
    )

    assert when_chunk is None
    assert given_sentence in when_current


def test_process_sentence_overflow():
    given_sentence = "Test sentence."
    given_current = ["Previous sentence."]
    given_length = len(tokenizer.encode("Previous sentence."))
    chunk_sz = len(tokenizer.encode("Previous sentence."))

    when_current, when_length, when_chunk = _process_sentence(
        given_sentence, given_current, given_length, chunk_sz=chunk_sz
    )

    then_expected_chunk = "Previous sentence."
    assert when_chunk == then_expected_chunk
    assert when_current == ["Test sentence."]
    assert when_length == len(tokenizer.encode("Test sentence."))


def test_exceeds_memory_limit():
    given_text = "word " * 1000

    when_result = _exceeds_memory_limit(given_text, chunk_sz=100, max_memory=5)

    assert when_result is True


def test_is_uninformative():
    given_short_chunk = "hi"
    given_normal_chunk = "This is a normal length chunk of text"
    given_special_chars = "⌘⌘⌘⌘⌘⌘⌘⌘⌘⌘⌘⌘"
    given_empty_chunk = ""
    given_whitespace_chunk = "   "

    assert _is_uninformative(given_short_chunk) is True
    assert _is_uninformative(given_normal_chunk) is False
    assert _is_uninformative(given_special_chars) is True
    assert _is_uninformative(given_empty_chunk) is True
    assert _is_uninformative(given_whitespace_chunk) is True


def test_create_chunks_multiple():
    given_text = """
    This is the first paragraph with multiple sentences. Here is another sentence.

    This is the second paragraph. It also has multiple parts to it.

    Finally a third paragraph. With even more sentences. And a final one.
    """

    when_chunks = create_chunks(text=given_text, chunk_sz=15)

    then_expected = [
        "This is the first paragraph with multiple sentences. Here is another sentence.",
        "This is the second paragraph. It also has multiple parts to it.",
        "Finally a third paragraph. With even more sentences. And a final one.",
    ]
    assert when_chunks == then_expected
