import datetime as dt
from typing import List

from src.bot.keyboards import main_kb
from src.models.contact import MContact
from src.models.log import MLog, MLogWithNumbers


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
            row = f'- {contact.name}'
            if contact.telegram:
                row += f' ({contact.telegram})'
            rows.append(row)
        return "\n".join(sorted(rows))

    def strip_log_text_list(self, logs_strs: List[str]) -> List[str]:
        return [self.strip_log_text(log_str) for log_str in logs_strs]

    def strip_log_text(self, log_str: str) -> str:
        log_str = log_str.strip()
        if len(log_str) == 0:
            return ""
        if log_str[0] == '-' or log_str[0] == '—' or log_str[0] == '–':
            log_str = log_str[1:]
        return log_str.strip()

    def convert_str_to_date(self, date_str: str) -> dt.datetime:
        """
        input = 'YYYY-MM-DD'
        output: dt.datetime.date (?)
        """
        pass

    def convert_date_to_str(self, date: dt.datetime) -> str:
        """
        input = dt.datetime.date | dt.datetime.datetime
        output: str
        """
        pass

    def __get_logs_with_dashes(self, logs: List[MLogWithNumbers] | List[MLog]) -> str:
        if isinstance(logs[0], MLogWithNumbers):
            log_texts_with_dashes = [f'{log.telegram_number}. {log.text}' for log in logs if log.text != ""]
        elif isinstance(logs[0], MLog):
            log_texts_with_dashes = [f'- {log.text}' for log in logs if log.text != ""]
        else:
            raise Exception(f'Unsupported type {type(logs)} for logs')

        return '\n'.join(log_texts_with_dashes)


telegram_service = TelegramService()
