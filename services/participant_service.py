# services/participant_service.py
from database.db import SessionLocal
from models.participant import Participant
from models.event import Event

class ParticipantService:
    def register_participant(self, event_id, name):
        session = SessionLocal()
        try:
            event = session.query(Event).filter(Event.id == event_id).first()
            if not event:
                return None
            participant = Participant(name=name, event_id=event_id)
            session.add(participant)
            session.commit()
            session.refresh(participant)
            return participant.to_dict()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_attendees(self, event_id):
        session = SessionLocal()
        try:
            event = session.query(Event).filter(Event.id == event_id).first()
            if not event:
                return None
            return [participant.to_dict() for participant in event.participants]
        finally:
            session.close()

    def edit_participant(self, participant_id, new_name):
        session = SessionLocal()
        try:
            participant = session.query(Participant).filter(Participant.id == participant_id).first()
            if not participant:
                return None
            participant.name = new_name
            session.commit()
            return participant.to_dict()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
