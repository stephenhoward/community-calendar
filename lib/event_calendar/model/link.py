from sqlalchemy import Column, String, Enum
import enum
from event_calendar.database import Base
from event_calendar.model import Model
from event_calendar.model.content import Content

LinkType = enum.Enum( 'LinkType', [
    'Information',
    'Tickets',
    'RSVP'
])

class Link(Content,Model,Base):
    __tablename__ = 'links'

    url       = Column( String )
    type      = Column( Enum(LinkType) )