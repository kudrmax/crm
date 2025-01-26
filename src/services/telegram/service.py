from typing import List

from src.models.log.models import MLog


class TelegramService:
    def convert_logs_to_str(self, logs: List[MLog]):
        log_texts = [log.text for log in logs]
        log_texts_with_dashes = [f'- {log_text}' for log_text in log_texts]
        log_texts_str = "\n".join(log_texts_with_dashes)
        return f"Logs:\n\n{log_texts_str}"


telegram_service = TelegramService()
