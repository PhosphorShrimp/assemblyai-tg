from app.services.transcript_formatter import format_transcript_payload


def test_format_transcript_payload_with_utterances() -> None:
    payload = {
        "id": "tr_123",
        "text": "Hello world",
        "utterances": [
            {"speaker": "A", "text": "Hello"},
            {"speaker": "B", "text": "world"},
        ],
    }

    formatted = format_transcript_payload(payload)

    assert formatted.transcript_id == "tr_123"
    assert formatted.full_text == "Hello world"
    assert len(formatted.utterances) == 2
    assert formatted.utterances[0].speaker == "A"
