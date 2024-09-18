import uuid

from sqlalchemy import Column, Integer, UUID, String

from src.database import Base


class MUser(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), nullable=False)
    password_hashed = Column(String(255), nullable=False)
