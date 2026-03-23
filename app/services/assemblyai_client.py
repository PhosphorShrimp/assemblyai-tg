"""AssemblyAI API client for file upload and transcription polling."""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import requests

logger = logging.getLogger(__name__)


class AssemblyAIUploadError(Exception):
    """Raised when upload to AssemblyAI fails."""


class AssemblyAIPollingError(Exception):
    """Raised when transcript polling fails."""


@dataclass(frozen=True)
class AssemblyAIClient:
    """Synchronous client for AssemblyAI pre-recorded transcription."""

    api_key: str
    base_url: str
    poll_interval_seconds: float

    def _headers(self) -> dict[str, str]:
        return {
            "authorization": self.api_key,
        }

    def upload_file(self, local_path: Path) -> str:
        """Upload local audio file and return AssemblyAI upload URL."""
        url = f"{self.base_url}/v2/upload"
        logger.info("Uploading file to AssemblyAI: %s", local_path)
        try:
            with local_path.open("rb") as binary:
                response = requests.post(url, headers=self._headers(), data=binary, timeout=120)
            response.raise_for_status()
            payload = response.json()
            upload_url = payload.get("upload_url")
            if not upload_url:
                raise AssemblyAIUploadError("No upload_url in AssemblyAI response")
            return upload_url
        except requests.RequestException as exc:
            raise AssemblyAIUploadError(str(exc)) from exc

    def create_transcript(self, audio_url: str) -> str:
        """Create transcript job and return transcript id."""
        url = f"{self.base_url}/v2/transcript"
        payload = {
            "audio_url": audio_url,
         "speech_models": ["universal-2"],
          "language_code": "ru",
         "speaker_labels": False,
        }  
        logger.info("Creating transcript job in AssemblyAI")
        try:
            response = requests.post(
                url,
                headers={**self._headers(), "content-type": "application/json"},
                json=payload,
                timeout=60,
            )
            response.raise_for_status()
            transcript_id = response.json().get("id")
            if not transcript_id:
                raise AssemblyAIPollingError("No transcript id in create response")
            return transcript_id
        except requests.RequestException as exc:
            raise AssemblyAIUploadError(str(exc)) from exc

    def poll_transcript(self, transcript_id: str) -> dict[str, Any]:
        """Poll transcript job until completion and return full payload."""
        url = f"{self.base_url}/v2/transcript/{transcript_id}"
        logger.info("Polling transcript job: %s", transcript_id)

        while True:
            try:
                response = requests.get(url, headers=self._headers(), timeout=30)
                response.raise_for_status()
                payload = response.json()
            except requests.RequestException as exc:
                raise AssemblyAIPollingError(str(exc)) from exc

            status = payload.get("status")
            if status == "completed":
                return payload
            if status == "error":
                error_msg = payload.get("error", "unknown transcription error")
                raise AssemblyAIPollingError(error_msg)

            time.sleep(self.poll_interval_seconds)
