# models/event.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.db import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date = Column(String, nullable=False)
    budget = Column(Integer, default=0)

    # Relacionamentos com tabelas filhas
    participants = relationship("Participant", back_populates="event", cascade="all, delete-orphan")
    speakers = relationship("Speaker", back_populates="event", cascade="all, delete-orphan")
    vendors = relationship("Vendor", back_populates="event", cascade="all, delete-orphan")
    feedbacks = relationship("Feedback", back_populates="event", cascade="all, delete-orphan")

    def __init__(self, name, date, budget=0):
        self.name = name
        self.date = date
        self.budget = budget

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "budget": self.budget,
            "participants": [p.to_dict() for p in self.participants],
            "speakers": [s.to_dict() for s in self.speakers],
            "vendors": [v.to_dict() for v in self.vendors],
            "feedbacks": [f.to_dict() for f in self.feedbacks]
        }
