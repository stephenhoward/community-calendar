from sqlalchemy import Column, Table, String, Text, Enum, DateTime, ForeignKey, tuple_
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
import enum
from event_calendar.model.content import Model
from event_calendar.model.content import PrimaryContentModel, TranslationModel
from event_calendar.database import Base
import event_calendar.model.location

events_categories_table = Table('events_categories', Base.metadata,
    Column('event_id',    UUID(as_uuid=True), ForeignKey('events.id')),
    Column('category_id', UUID(as_uuid=True), ForeignKey('categories.id'))
)

EventRepeat = enum.Enum( 'EventRepeat', [
    'Once',
    'Daily',
    'Weekly',
    'Monthly',
    'MonthlyByDayOfWeek'
])

class Event(PrimaryContentModel,Base):
    __tablename__ = 'events'

    location_id = Column( UUID(as_uuid=True), ForeignKey('locations.id') )
    series_id   = Column( UUID(as_uuid=True), ForeignKey('series.id') )

    info       = relationship( "EventInfo", lazy='joined' )
    categories = relationship( "Category", secondary=events_categories_table )
    location   = relationship( "Location" )
    series     = relationship( "Series", backref="events" )
    dates      = relationship( "EventDate", back_populates="event" )

    @classmethod
    def _search(cls,query,**kwargs):
        if ( 'from' in kwargs and 'to' in kwargs ):
            query = query.filter(  tuple_(cls.start,cls.end).op( 'overlaps' )( tuple_(kwargs['from'], kwargs['to']) )  )
        elif( 'from' in kwargs ):
            query = query.filter( cls.end > kwargs['from'] )
        elif( 'to' in kwargs ):
            query = query.filter( cls.start < kwargs['to'] )

        return query

    def dump(self):
        d = super().dump()

        d['categories'] = list(map( lambda x: x.dump(), self.categories ))

        return d

class EventDate(Model,Base):
    __tablename__ = 'events_dates'

    event_id        = Column( UUID(as_uuid=True), ForeignKey('events.id') )
    start_time      = Column( DateTime )
    end_time        = Column( DateTime )
    repeat_interval = Column( Enum(EventRepeat) )

    event = relationship("Event")

# for translatable parts of the event
class EventInfo(TranslationModel,Base):
    __tablename__ = 'events_i18n'

    id          = Column( UUID(as_uuid=True), ForeignKey('events.id'), primary_key=True )
    title       = Column( Text )
    description = Column( Text )
    accessibility_information = Column( Text )

    event = relationship( "Event" )

