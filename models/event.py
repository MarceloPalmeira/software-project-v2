from sqlalchemy import Column, Integer, String
from database.db import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date = Column(String, nullable=False)
    budget = Column(Integer, default=0)

    def __init__(self, name, date, budget=0):  # Corrigido: Sem `id`
        self.name = name
        self.date = date
        self.budget = budget

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "date": self.date,
            "budget": self.budget
        }
