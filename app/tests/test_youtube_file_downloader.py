from app.youtube_url_downloader import is_youtube_url


def test_is_youtube_url():
    assert is_youtube_url("https://www.youtube.com/watch?v=8OAPLk20epo")
    assert is_youtube_url("http://youtube.com/watch?v=8OAPLk20epo")
    assert is_youtube_url("www.youtube.com/watch?v=8OAPLk20epo")
    assert is_youtube_url("youtube.com/watch?v=8OAPLk20epo")
    assert is_youtube_url("https://youtu.be/8OAPLk20epo")
    assert is_youtube_url("https://www.youtube-nocookie.com/embed/8OAPLk20epo")

    assert not is_youtube_url("https://www.example.com/watch?v=8OAPLk20epo")
    assert not is_youtube_url("https://www.youtubee.com/watch?v=8OAPLk20epo")
    assert not is_youtube_url("https://www.youtu.be.com/watch?v=8OAPLk20epo")
