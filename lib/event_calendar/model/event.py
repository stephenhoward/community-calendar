from sqlalchemy import Column, Table, String, Text, Enum, Boolean, DateTime, ForeignKey, tuple_
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
import enum
from event_calendar.model import TranslatableModel, Translation, ContentStatus
from event_calendar.database import Base
import event_calendar.model.location
import event_calendar.model.user
import event_calendar.model.comment
from event_calendar.model.link import EventLink

event_categories_table = Table('event_categories', Base.metadata,
    Column('event_id',    UUID(as_uuid=True), ForeignKey('events.id')),
    Column('category_id', UUID(as_uuid=True), ForeignKey('categories.id'))
)

EventAge = enum.Enum( 'EventAge', [
    '21+',
    '18+',
    'All Ages',
    'Youth',
    'Big Kids',
    'Little Kids',
    'Kids'
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

class Event(TranslatableModel,Base):
    __tablename__ = 'events'

    id            = Column( UUID(as_uuid=True), primary_key=True )
    status        = Column( Enum(ContentStatus) )
    start         = Column( DateTime )
    end           = Column( DateTime )
    dates_only    = Column( Boolean )
    repeat        = Column( Enum(EventRepeat) )
    repeat_by     = Column( Enum(EventRepeatBy) )
    location_id   = Column( UUID(as_uuid=True), ForeignKey('locations.id') )
    contact_phone = Column( String )
    contact_email = Column( String )
    series_id     = Column( UUID(as_uuid=True), ForeignKey('series.id') )

    urls       = relationship( "EventLink" )
    info       = relationship( "EventInfo", lazy='joined' )
    categories = relationship( "Event", secondary=event_categories_table )
    images     = relationship( "EventImage" )
    location   = relationship( "Location" )
    comments   = relationship( "EventComment", back_populates="event" )
    series     = relationship( "Series", back_populates="events" )

    @classmethod
    def _search(cls,query,**kwargs):
        if ( 'from' in kwargs and 'to' in kwargs ):
            query = query.filter(  tuple_(cls.start,cls.end).op( 'overlaps' )( tuple_(kwargs['from'], kwargs['to']) )  )
        elif( 'from' in kwargs ):
            query = query.filter( cls.end > kwargs['from'] )
        elif( 'to' in kwargs ):
            query = query.filter( cls.start < kwargs['to'] )

        return query

# for translatable parts of the event
class EventInfo(Translation,Base):
    __tablename__ = 'events_i18n'

    id          = Column( UUID(as_uuid=True), ForeignKey('events.id'), primary_key=True )
    title       = Column( Text )
    description = Column( Text )
    accessibility_information = Column( Text )

    event = relationship( "Event" )

