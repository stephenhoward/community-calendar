import datetime
from sqlalchemy import Column, Table, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from event_calendar.model import Model
from event_calendar.database import Base
from event_calendar.config import config
from event_calendar.email import EmailSender

class PasswordToken(Model,Base):
    __tablename__ = 'password_tokens'

    user_id = Column( UUID(as_uuid=True), ForeignKey('users.id') )
    created = Column( DateTime, default = datetime.datetime.utcnow )
    expires = Column( DateTime )
    user    = relationship( "User" )

    @classmethod
    def generate(cls,user):

        existing_token = cls.search(
            cls.user_id == user.id,
            cls.expires >= datetime.datetime.utcnow()
        ).first()

        if existing_token is not None:
            return existing_token
        else:
            t = cls.create({
                'user_id': user.id,
                'expires': datetime.datetime.utcnow() + datetime.timedelta( seconds = config.get('password_reset','expires'))
            })
            t.save()

            return t

    @classmethod
    def retrieve(cls,token_id):
        return cls.search(
            cls.id      == token_id,
            cls.expires >= datetime.datetime.utcnow()
        ).first()

    def send(self):

        EmailSender().send_template(
            to       = self.user.email,
            template = 'email/password_reset.txt',
            lang     = self.user.language.name,
            args     = {
                'user':  self.user,
                'token': self.id
            }
        )

    def expire(self):
        self.expires = datetime.datetime.utcnow()
        self.save()

    def _dont_dump(self):
        return ['id'];
