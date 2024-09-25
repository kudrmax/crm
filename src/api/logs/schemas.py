import datetime as dt
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.v1 import validator


class SLogRead(BaseModel):
    id: int
    contact_id: UUID | None = None
    datetime: dt.datetime
    log: str
    number: str | None = None


class SLogsOnDate(BaseModel):
    data: str
    logs: List[SLogRead]


class SLogCreate(BaseModel):
    name: str
    log: str


class SLogCreateOnDate(SLogCreate):
    date: dt.date


class SEmptyLogCreate(BaseModel):
    name: str


class SLogUpdate(BaseModel):
    log: str | None = None
    datetime: dt.datetime | None = None
