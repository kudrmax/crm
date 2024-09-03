import uuid

from sqlalchemy import UUID, Column, String, Date, Integer, ForeignKey, DateTime

from src.database import Base


class MLog(Base):
    __tablename__ = "log"

    id = Column(Integer, primary_key=True)
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id"), nullable=False)
    datetime = Column(DateTime, nullable=False)
    text = Column(String, nullable=True)
