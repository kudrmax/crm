import datetime
from uuid import UUID

from pydantic import BaseModel


class SContactRead(BaseModel):
    name: str | None = None
    phone: str | None = None
    telegram: str | None = None
    birthday: datetime.date | None = None


class SContactCreate(BaseModel):
    name: str


class SContactUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    telegram: str | None = None
    birthday: datetime.date | None = None
