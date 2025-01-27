from typing import List

from src.models.log.models import MLog, MLogWithNumbers


class TelegramService:
    def convert_logs_to_str(self, logs: List[MLogWithNumbers] | List[MLog]):
        if len(logs) == 0:
            return "No logs"
        if isinstance(logs[0], MLogWithNumbers):
            log_texts_with_dashes = [f'{log.telegram_number}. {log.text}' for log in logs if log.text != ""]
        elif isinstance(logs[0], MLog):
            log_texts_with_dashes = [f'- {log.text}' for log in logs if log.text != ""]
        else:
            raise Exception(f'Unsupported type {type(logs)}')
        log_texts_str = "\n".join(log_texts_with_dashes)
        return f"Logs:\n\n{log_texts_str}"


telegram_service = TelegramService()
