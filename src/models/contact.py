import dataclasses
import datetime as dt
import re


@dataclasses.dataclass
class MContact:
    id: int = None
    name: str = None
    phone: str = None
    telegram: str = None
    birthday: str = None

    # created_at: dt.datetime = None
    # updated_at: dt.datetime = None

    def to_string(self) -> str:
        result = [
            f"*{escape_markdown_v2(self.name)}*",
            ""
        ]
        if self.telegram:
            telegram = self.telegram
            telegram = escape_markdown_v2(telegram)
            result.append(f"✈️ Telegram: {telegram}")
        if self.phone:
            phone = self.phone
            phone = escape_markdown_v2(phone)
            result.append(f"📞 Phone: {phone}")
        if self.birthday:
            birthday = self.birthday
            birthday = escape_markdown_v2(birthday)
            result.append(f"🎉 Birthday: {birthday}")

        return "\n".join(result)


@dataclasses.dataclass
class MContactCreate:
    name: str = None
    phone: str = None
    telegram: str = None
    birthday: dt.datetime = None


@dataclasses.dataclass
class MContactUpdate:
    name: str = None
    phone: str = None
    telegram: str = None
    birthday: dt.datetime = None


def escape_markdown_v2(text: str | None = None) -> str:
    if not text:
        return text
    return re.sub(r'([_*\[\]()~`>#+\-=|{}.!])', r'\\\1', text)


def create_spoiler(text: str) -> str:
    return '||' + text + '||'
