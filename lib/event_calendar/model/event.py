from sqlalchemy import Column, Table, String, Text, Enum, Boolean, DateTime, ForeignKey, tuple_
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
import enum
from event_calendar.model import Model, Translation
from event_calendar.database import Base
import event_calendar.model.image
import event_calendar.model.location
import event_calendar.model.user

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

    id            = Column( UUID(as_uuid=True), primary_key=True )
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
    info       = relationship( "EventInfo", lazy='joined' )
    categories = relationship( "Event", secondary=event_categories_table )
    images     = relationship( "EventImage" )
    events     = relationship( "Event", backref=backref("parent", remote_side=[id])  )
    location   = relationship( "Location" )
    comments   = relationship( "EventComment", back_populates="event" )

    @classmethod
    def _search(cls,query,**kwargs):
        if ( 'from' in kwargs and 'to' in kwargs ):
            query = query.filter(  tuple_(cls.start,cls.end).op( 'overlaps' )( tuple_(kwargs['from'], kwargs['to']) )  )
        elif( 'from' in kwargs ):
            query = query.filter( cls.end > kwargs['from'] )
        elif( 'to' in kwargs ):
            query = query.filter( cls.start < kwargs['to'] )

        return query

class EventLink(Model,Base):
    __tablename__ = 'event_links'

    event_id = Column( UUID(as_uuid=True), ForeignKey('events.id') )
    url      = Column( String )
    type     = Column( Enum(LinkType) )

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

    id        = Column( UUID(as_uuid=True), primary_key=True )
    when      = Column( DateTime )
    edited    = Column( Boolean )
    event_id  = Column( UUID(as_uuid=True), ForeignKey('events.id') )
    author_id = Column( UUID(as_uuid=True), ForeignKey('users.id') )
    parent_id = Column( UUID(as_uuid=True), ForeignKey('event_comments.id') )
    contents  = Column( Text )

    event     = relationship( "Event", back_populates="comments" )
    author    = relationship( "User" )
    children  = relationship( "EventComment", backref=backref("parent", remote_side=[id])  )

