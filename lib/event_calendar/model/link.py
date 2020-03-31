from sqlalchemy import Column, String, Enum
import enum
from event_calendar.database import Base
from event_calendar.model import Model
from event_calendar.model.content import ContentMixin

LinkType = enum.Enum( 'LinkType', [
    'Information',
    'Tickets',
    'RSVP'
])

class Link(ContentMixin,Model,Base):
    __tablename__ = 'links'

    url       = Column( String )
    type      = Column( Enum(LinkType) )