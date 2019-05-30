from sqlalchemy import Column, Table, String, Text, Enum, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
import enum
from event_calendar.model import Model, Translation
from event_calendar.database import Base

event_categories_table = Table('event_categories', Base.metadata,
    Column('event_id',    UUID(as_uuid=True), ForeignKey('events.id')),
    Column('category_id', UUID(as_uuid=True), ForeignKey('categories.id'))
)

EventStatus = enum.Enum( 'EventStatus', [
    'Draft',
    'Active'
])

EventRepeat = enum.Enum( 'EventRepeat', [
    'Daily',
    'Weekly',
    'Monthly'
])

EventRepeatBy = enum.Enum( 'EventRepeatBy', [
    'DayOfMonth',    # 12th of each month
    'WeekdayOfMonth' # First Tuesday of each month
])

LinkType = enum.Enum( 'LinkType', [
    'Information',
    'Tickets',
    'RSVP'
])

class Event(Model,Base):
    __tablename__ = 'events'

    status        = Column( Enum(EventStatus) )
    start         = Column( DateTime )
    end           = Column( DateTime )
    dates_only    = Column( Boolean )
    repeat        = Column( Enum(EventRepeat) )
    repeat_by     = Column( Enum(EventRepeatBy) )
    location_id   = Column( UUID(as_uuid=True), ForeignKey('locations.id') )
    contact_phone = Column( String )
    contact_email = Column( String )
    parent_id     = Column( UUID(as_uuid=True), ForeignKey('events.id') )

    urls       = relationship( "EventLink" )
    info       = relationship( "EventInfo" )
    categories = relationship( "Event", secondary=event_categories_table )
    images     = relationship( "Image" )
    events     = relationship( "Event" )
    location   = relationship( "Location" )
    comments   = relationship( "EventComment", back_populates="event" )

class EventLink(Model,Base):
    __tablename__ = 'event_links'

    event_id = Column( UUID(as_uuid=True), ForeignKey('events.id') )
    url = Column( String )
    type = Column( Enum(LinkType) )

# for translatable parts of the event
class EventInfo(Translation,Base):
    __tablename__ = 'events_i18n'

    id          = Column( UUID(as_uuid=True), ForeignKey('events.id'), primary_key=True )
    title       = Column( Text )
    description = Column( Text )
    accessibility_information = Column( Text )

    event = relationship( "Event" )

# for internal discussion of drafted events:
class EventComment(Model,Base):
    __tablename__ = 'event_comments'

    when      = Column( DateTime )
    edited    = Column( Boolean )
    event_id  = Column( UUID(as_uuid=True), ForeignKey('events.id') )
    author_id = Column( UUID(as_uuid=True), ForeignKey('users.id') )
    parent_id = Column( UUID(as_uuid=True), ForeignKey('event_comments.id') )
    contents  = Column( Text )
    event          = relationship( "Event" )
    author         = relationship( "User" )
    parent_comment = relationship( "EventComment" )
    child_comments = relationship( "EventComment" )

