from sqlalchemy import Column, Integer, String
from database.db import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date = Column(String, nullable=False)
    budget = Column(Integer, default=0)
    participants = Column(String, nullable=True)
    speakers = Column(String, nullable=True)
    vendors = Column(String, nullable=True)
    feedback = Column(String, nullable=True)

    def __init__(self, name, date, budget=0, participants=None, speakers=None, vendors=None, feedback=None):
        self.name = name
        self.date = date
        self.budget = budget
        self.participants = participants
        self.speakers = speakers
        self.vendors = vendors
        self.feedback = feedback

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "budget": self.budget,
            "participants": self.participants,
            "speakers": self.speakers,
            "vendors": self.vendors,
            "feedback": self.feedback
        }
