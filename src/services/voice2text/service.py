from src.services.voice2text.google_api.service import GoogleAPIVoice2TextService
from src.services.voice2text.whisper.service import WhisperVoice2TextService


class Voice2TextService:
    def __init__(self, voice2text_service):
        self.voice2text_service = voice2text_service

    def voice2text(self, file_path: str) -> str:
        return self.voice2text_service.voice2text(file_path)


voice2text_service = Voice2TextService(WhisperVoice2TextService())
