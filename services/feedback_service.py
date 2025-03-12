# services/feedback_service.py
from database.db import SessionLocal
from models.feedback import Feedback
from models.event import Event

class FeedbackService:
    def add_feedback(self, event_id, content):
        session = SessionLocal()
        try:
            event = session.query(Event).filter(Event.id == event_id).first()
            if not event:
                return None
            feedback = Feedback(content=content, event_id=event_id)
            session.add(feedback)
            session.commit()
            session.refresh(feedback)
            return feedback.to_dict()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
