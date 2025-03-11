# models/feedback.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    event = relationship("Event", back_populates="feedbacks")

    def __init__(self, content, event_id):
        self.content = content
        self.event_id = event_id

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "event_id": self.event_id
        }
