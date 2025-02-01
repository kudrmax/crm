import whisper

from src.services.voice2text.decorators import print_decorator, timing_decorator


class WhisperVoice2TextService:
    def __init__(self):
        self.model = whisper.load_model("base", device="cpu")  # Choose: tiny, base, small, medium, large

    @print_decorator
    @timing_decorator
    def voice2text(self, file_path) -> str:
        """
        OpenAI Whisper

        Accuracy: High
        Speed: Medium/Slow
        Internet Required: No
        """
        result = self.model.transcribe(file_path, fp16=False)
        return result["text"].strip()
