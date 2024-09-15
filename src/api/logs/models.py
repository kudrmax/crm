import uuid

import datetime
from sqlalchemy import UUID, Column, String, Date, Integer, ForeignKey, DateTime, func, TIMESTAMP

from src.database import Base


class MLog(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True)
    contact_id = Column(UUID(as_uuid=True), ForeignKey('contacts.id', ondelete="CASCADE"), nullable=False)
    # datetime = Column(DateTime, server_default=func.current_timestamp(), nullable=False)
    datetime = Column(DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.timezone.utc))
    log = Column(String, nullable=False, default="")
