import dataclasses
import datetime as dt


@dataclasses.dataclass
class MLog:
    id: int = None
    contact_id: int = None
    text: str = None
    datetime: dt.datetime = None


@dataclasses.dataclass
class MLogCreate:
    contact_id: int = None
    text: str = None
    datetime: dt.datetime = dt.datetime.now()


@dataclasses.dataclass
class MLogUpdate:
    contact_id: int = None
    text: str = None
    datetime: dt.datetime = None


@dataclasses.dataclass
class MLogWithNumbers(MLog):
    telegram_number: int = None
