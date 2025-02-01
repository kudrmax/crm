import datetime as dt
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

        logs = sorted(logs, key=lambda l: l.datetime)

        date_to_logs_list = {}
        for log in logs:
            date = log.datetime.date()
            if date not in date_to_logs_list:
                date_to_logs_list[date] = []
            date_to_logs_list[date].append(log)

        logs_grouped_by_date = []
        for date in date_to_logs_list.keys():
            logs = date_to_logs_list[date]
            logs_with_dame_date = self.__get_logs_with_dashes(logs)
            date_str = f'{date.year:04}-{date.month:02}-{date.day:02}:\n'
            logs_grouped_by_date.append(date_str + logs_with_dame_date)
        return "\n\n".join(logs_grouped_by_date)

    def get_all_contacts_post(self, contacts: List[MContact]):
        rows = []
        for contact in contacts:
            row = f'— {contact.name}'
            if contact.telegram:
                row += f' ({contact.telegram})'
            rows.append(row)
        return "\n".join(sorted(rows))

    def __get_logs_with_dashes(self, logs: List[MLogWithNumbers] | List[MLog]) -> str:
        if isinstance(logs[0], MLogWithNumbers):
            log_texts_with_dashes = [f'{log.telegram_number}. {log.text}' for log in logs if log.text != ""]
        elif isinstance(logs[0], MLog):
            log_texts_with_dashes = [f'- {log.text}' for log in logs if log.text != ""]
        else:
            raise Exception(f'Unsupported type {type(logs)} for logs')

        return '\n'.join(log_texts_with_dashes)


telegram_service = TelegramService()
