from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Integer,
    Text,
    text,
)

from sqlalchemy.dialects.postgresql import ARRAY
from .Base import Base


class Metric(Base):
    __tablename__ = 'telemetry'

    id = Column(BigInteger, primary_key=True)

    created = Column(DateTime, nullable=False, index=True)
    delivered = Column(DateTime, server_default=text('now()'), nullable=False)

    metric = Column(Integer, index=True, nullable=False)
    key = Column(Integer, index=True, nullable=False)
    value = Column(BigInteger, nullable=False)

    labels = Column(ARRAY(Text), nullable=False)

    def __repr__(self):
        return f'<Metric {self.id}>'
