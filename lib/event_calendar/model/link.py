from sqlalchemy import Column, Table, String, Text, Enum, Boolean, DateTime, ForeignKey, tuple_
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
import enum
from event_calendar.model import Model, Translation
from event_calendar.database import Base
import event_calendar.model.image
import event_calendar.model.location
import event_calendar.model.user

LinkType = enum.Enum( 'LinkType', [
    'Information',
    'Tickets',
    'RSVP'
])

class Link(Model):
    url       = Column( String )
    type      = Column( Enum(LinkType) )

class EventLink(Model,Base):
    __tablename__ = 'event_links'

    event_id = Column( UUID(as_uuid=True), ForeignKey('events.id') )

class SeriesLink(Model,Base):
    __tablename__ = 'series_links'

    series_id = Column( UUID(as_uuid=True), ForeignKey('series.id') )

