from unittest.mock import mock_open, patch
import json

from app.memory import (
    process_chunk,
    load_info,
    memorize,
    get_summary,
    store_info
)

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

@patch('app.memory.process_chunk')
@patch('jsonlines.open')
@patch('time.sleep')
def test_store_info(mock_sleep, mock_jsonlines_open, mock_process_chunk):
    # given
    chunks = ["chunk1", "chunk2"]
    mock_process_chunk.side_effect = lambda chunk, info: info + [{"processed": chunk}]
    mock_file = mock_jsonlines_open.return_value.__enter__.return_value
    
    # when
    store_info(chunks, "test_path.json")
    
    #then
    assert mock_process_chunk.call_count == 2
    assert mock_sleep.call_count == 2
    mock_file.write.assert_called_once_with([{"processed": "chunk1"}, {"processed": "chunk2"}])

