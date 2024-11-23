from app.input_reader import _is_youtube_url, get_text
import pytest


def test_get_text_url(mocker):
    test_url = "https://www.example.com"
    mock_process_url = mocker.patch('app.input_reader.process_url')

    get_text(test_url)
    mock_process_url.assert_called_once_with(test_url)


def test_get_text_youtube_url(mocker):
    test_youtube_url = "https://www.youtube.com/watch?v=8OAPLk20epo"
    mock_download_audio = mocker.patch('app.input_reader.download_audio')
    mock_process_audio = mocker.patch('app.input_reader.process_audio')

    get_text(test_youtube_url)
    mock_download_audio.assert_called_once_with(test_youtube_url)
    mock_process_audio.assert_called_once()


def test_get_text_epub(mocker):
    test_epub_path = "path/to/test_epub.epub"
    mock_process_epub = mocker.patch('app.input_reader.process_epub')

    get_text(test_epub_path)
    mock_process_epub.assert_called_once_with(test_epub_path)


def test_get_text_pdf(mocker):
    test_pdf_path = "path/to/test_pdf.pdf"
    mock_process_pdf = mocker.patch('app.input_reader.process_pdf')

    get_text(test_pdf_path)
    mock_process_pdf.assert_called_once_with(test_pdf_path)


def test_get_text_doc(mocker):
    test_doc_path = "path/to/test_doc.doc"
    mock_process_doc = mocker.patch('app.input_reader.process_doc')

    get_text(test_doc_path)
    mock_process_doc.assert_called_once_with(test_doc_path)


def test_get_text_txt(mocker):
    test_txt_path = "path/to/test_txt.txt"
    mock_process_txt = mocker.patch('app.input_reader.process_txt')

    get_text(test_txt_path)
    mock_process_txt.assert_called_once_with(test_txt_path)


def test_get_text_audio(mocker):
    test_audio_path = "path/to/test_audio.wav"
    mock_process_audio = mocker.patch('app.input_reader.process_audio')

    get_text(test_audio_path)
    mock_process_audio.assert_called_once_with(test_audio_path)


def test_get_text_unsupported_file_type():
    unsupported_file_path = "path/to/unsupported_file.mp4"

    with pytest.raises(ValueError, match="Invalid document path!"):
        get_text(unsupported_file_path)


def test_is_youtube_url():
    valid_urls = [
        "https://www.youtube.com/watch?v=8OAPLk20epo",
        "http://youtube.com/watch?v=8OAPLk20epo",
        "https://youtu.be/8OAPLk20epo",
        "https://m.youtube.com/watch?v=8OAPLk20epo",
        "https://youtube.com/embed/8OAPLk20epo"
    ]

    invalid_urls = [
        "https://www.example.com/watch?v=8OAPLk20epo",
        "https://www.youtubee.com/watch?v=8OAPLk20epo",
        "https://www.youtu.be.com/watch?v=8OAPLk20epo"
    ]

    for url in valid_urls:
        assert _is_youtube_url(url), f"URL should be valid: {url}"

    for url in invalid_urls:
        assert not _is_youtube_url(url), f"URL should be invalid: {url}"
