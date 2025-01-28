from typing import List

from src.bot.keyboards import main_kb
from src.models.contact.model import MContact
from src.models.log.models import MLog, MLogWithNumbers


class MainMenuService:
    def get_post(self):
        return "Choose option:"

    def get_kb(self):
        return main_kb()


class TelegramService:
    main_menu: MainMenuService = MainMenuService()

    def get_logs_post(self, logs: List[MLogWithNumbers] | List[MLog], name: str | None = None) -> str:
        if len(logs) == 0:
            return f'👎🏻 There is no logs' if not name else f'👎🏻 There is no logs for {name}'

        if isinstance(logs[0], MLogWithNumbers):
            log_texts_with_dashes = [f'{log.telegram_number}. {log.text}' for log in logs if log.text != ""]
        elif isinstance(logs[0], MLog):
            log_texts_with_dashes = [f'- {log.text}' for log in logs if log.text != ""]
        else:
            raise Exception(f'Unsupported type {type(logs)}')

        log_texts_str = "\n".join(log_texts_with_dashes)
        title = "Logs:" if not name else f"Logs of {name}:"
        return f"{title}\n\n{log_texts_str}"

    def get_all_contacts_post(self, contacts: List[MContact]):
        rows = []
        for contact in contacts:
            row = f'— {contact.name}'
            if contact.telegram:
                row += f' ({contact.telegram})'
            rows.append(row)
        return "\n".join(sorted(rows))


telegram_service = TelegramService()
