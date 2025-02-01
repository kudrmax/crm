import whisper


class WhisperVoice2TextService:
    def __init__(self):
        model_size = "medium"
        self.model = whisper.load_model(model_size, device="cpu")  # Choose: tiny, base, small, medium, large

    def voice2text(self, file_path) -> str:
        """
        OpenAI Whisper

        Accuracy: High
        Speed: Medium/Slow
        Internet Required: No
        """
        result = self.model.transcribe(
            file_path,
            fp16=False,
            language="ru",
            # temperature=0.2,
            condition_on_previous_text=False,
        )
        return result["text"].strip()
