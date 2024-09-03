import uuid

from sqlalchemy import UUID, Column, String, Date, Integer, ForeignKey

from src.database import Base


class MContact(Base):
    __tablename__ = "contacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    phone = Column(String)
    telegram = Column(String)
    birthday = Column(Date)
    area = Column(String)
    log = Column(String)