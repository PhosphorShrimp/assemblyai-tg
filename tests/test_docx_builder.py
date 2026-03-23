from datetime import datetime

from docx import Document

from app.services.docx_builder import build_transcript_docx
from app.services.transcript_formatter import FormattedTranscript, SpeakerUtterance


def test_build_transcript_docx(tmp_path) -> None:
    output = tmp_path / "result.docx"
    transcript = FormattedTranscript(
        transcript_id="tr_123",
        full_text="Полный текст транскрипции",
        utterances=[SpeakerUtterance(speaker="1", text="Привет")],
    )

    build_transcript_docx(
        output_path=output,
        source_file_name="voice.ogg",
        transcript=transcript,
        processed_at=datetime(2026, 1, 1, 12, 0, 0),
    )

    assert output.exists()

    doc = Document(output)
    text = "\n".join(par.text for par in doc.paragraphs)
    assert "Транскрипция аудио" in text
    assert "voice.ogg" in text
    assert "tr_123" in text
    assert "Разбивка по спикерам" in text
