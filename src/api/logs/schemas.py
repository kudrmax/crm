import datetime as dt
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.v1 import validator


class SLogRead(BaseModel):
    id: int
    contact_id: UUID
    datetime: dt.datetime
    log: str


class SLogCreate(BaseModel):
    name: str
    log: str


class SEmptyLogCreate(BaseModel):
    name: str


class SLogUpdate(BaseModel):
    log: str | None = None
    # date: dt.datetime | None = None
