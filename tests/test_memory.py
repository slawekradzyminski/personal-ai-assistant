import pytest
from unittest.mock import mock_open, patch
import json

from app.memory import (
    is_uninformative,
    process_chunk,
    store_info,
    load_info,
    memorize,
    get_summary
)

def test_is_uninformative():
    # given
    short_chunk = "hi"
    normal_chunk = "This is a normal length chunk of text"
    special_chars = "⌘⌘⌘⌘⌘⌘⌘⌘⌘⌘⌘⌘"
    empty_chunk = ""
    whitespace_chunk = "   "
    
    # when/then
    assert is_uninformative(short_chunk) == True  # Too short
    assert is_uninformative(normal_chunk) == False  # Good length, normal text
    assert is_uninformative(special_chars) == True  # High token/char ratio
    assert is_uninformative(empty_chunk) == True  # Empty is uninformative
    assert is_uninformative(whitespace_chunk) == True  # Just whitespace is uninformative

@patch('app.memory.get_embeddings')
@patch('app.memory.get_summary')
def test_process_chunk(mock_get_summary, mock_get_embeddings):
    # given
    chunk = "This is a test chunk"
    info = []
    mock_get_summary.return_value = "Test summary"
    mock_get_embeddings.return_value = [0.1, 0.2, 0.3]

    # when
    result = process_chunk(chunk, info)

    # then
    assert len(result) == 1
    assert result[0]["text"] == chunk
    assert result[0]["summary"] == "Test summary"
    assert result[0]["embd"] == [0.1, 0.2, 0.3]
    assert result[0]["id"] == 0

def test_store_info_max_memory_exceeded():
    # given
    long_text = "word " * 1000
    memory_path = "test_memory.json"
    max_memory = 1

    # when/then
    with pytest.raises(ValueError, match="Processing is aborted due to high anticipated costs."):
        store_info(long_text, memory_path, chunk_sz=10, max_memory=max_memory)

def test_load_info():
    # given
    test_data = [{"id": 0, "text": "test", "summary": "test summary"}]
    mock_file = mock_open(read_data=json.dumps(test_data))
    
    # when
    with patch('builtins.open', mock_file):
        result = load_info("test_path.json")
    
    # then
    assert isinstance(result, list)
    assert len(result) == 1
    assert result[0]["text"] == "test"

@patch('os.path.exists')
@patch('app.memory.store_info')
def test_memorize_new_content(mock_store_info, mock_exists):
    # given
    test_text = "This is test content"
    mock_exists.return_value = False
    
    # when
    result = memorize(test_text)
    
    # then
    assert result.startswith("memory/")
    assert result.endswith(".json")
    mock_store_info.assert_called_once()

@patch('os.path.exists')
@patch('app.memory.store_info')
def test_memorize_cached_content(mock_store_info, mock_exists):
    # given
    test_text = "This is test content"
    mock_exists.return_value = True
    
    # when
    result = memorize(test_text)
    
    # then
    assert result.startswith("memory/")
    assert result.endswith(".json")
    mock_store_info.assert_not_called()

@patch('app.memory.api_get_completion')
def test_get_summary(mock_api_get_completion):
    # given
    test_chunk = "This is a test chunk"
    expected_summary = "Test summary"
    mock_api_get_completion.return_value = expected_summary
    
    # when
    result = get_summary(test_chunk)
    
    # then
    assert result == expected_summary
    mock_api_get_completion.assert_called_once()

