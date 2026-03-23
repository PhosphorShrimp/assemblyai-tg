from app.utils.mime import is_audio_document


def test_is_audio_document_by_mime_type() -> None:
    assert is_audio_document("file.bin", "audio/mpeg") is True


def test_is_audio_document_by_extension() -> None:
    assert is_audio_document("track.wav", None) is True


def test_is_audio_document_negative() -> None:
    assert is_audio_document("file.txt", "text/plain") is False
