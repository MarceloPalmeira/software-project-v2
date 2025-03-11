# models/vendor.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Vendor(Base):
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    services = Column(String, nullable=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    event = relationship("Event", back_populates="vendors")

    def __init__(self, name, services, event_id):
        self.name = name
        self.services = services
        self.event_id = event_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "services": self.services,
            "event_id": self.event_id
        }
