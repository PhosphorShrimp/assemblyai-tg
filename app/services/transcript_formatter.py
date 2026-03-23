"""Transcript formatting helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SpeakerUtterance:
    """Single speaker utterance line."""

    speaker: str
    text: str


@dataclass(frozen=True)
class FormattedTranscript:
    """Normalized transcript data for DOCX rendering."""

    transcript_id: str
    full_text: str
    utterances: list[SpeakerUtterance]


def format_transcript_payload(payload: dict[str, Any]) -> FormattedTranscript:
    """Normalize AssemblyAI transcript JSON into typed structure."""
    transcript_id = str(payload.get("id", "unknown"))
    full_text = str(payload.get("text", "")).strip()

    utterances_raw = payload.get("utterances") or []
    utterances: list[SpeakerUtterance] = []
    for item in utterances_raw:
        speaker = str(item.get("speaker", "Unknown"))
        text = str(item.get("text", "")).strip()
        if text:
            utterances.append(SpeakerUtterance(speaker=speaker, text=text))

    return FormattedTranscript(
        transcript_id=transcript_id,
        full_text=full_text,
        utterances=utterances,
    )
