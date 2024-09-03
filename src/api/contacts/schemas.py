import datetime
from uuid import UUID

from pydantic import BaseModel


class SContact(BaseModel):
    id: UUID
    name: str
    phone: str
    telegram: str
    birthday: datetime.date
    area: str
    log: str


class SContactCreate(BaseModel):
    name: str


class SContactUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None
    telegram: str | None = None
    birthday: datetime.date | None = None
    area: str | None = None
