# models/participant.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Participant(Base):
    __tablename__ = "participants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    # Relacionamento reverso
    event = relationship("Event", back_populates="participants")

    def __init__(self, name, event_id):
        self.name = name
        self.event_id = event_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "event_id": self.event_id
        }
