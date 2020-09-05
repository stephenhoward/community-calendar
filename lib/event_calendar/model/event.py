from sqlalchemy import Column, Table, String, Text, Enum, DateTime, ForeignKey, tuple_
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
import enum
import datetime
from dateutil import relativedelta, rrule
from event_calendar.database import DB
from event_calendar.model.content import Model
from event_calendar.model.content import PrimaryContentModel, TranslationModel
from event_calendar.database import Base
from event_calendar.model.category import Category
from event_calendar.model.series import Series
import event_calendar.model.location

db = DB()

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
    instances  = relationship( "EventDateInstance", back_populates="event" )

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
    repeat_end      = Column( DateTime )

    event = relationship("Event")

    def save(self):
        super().save()
        self.create_instances()

    def delete(self):
        super().delete()
        self.destroy_instances()

    def create_instances(self):

        self.destroy_instances( fromNow = True)

        end_time_delta = relative_delta( self.end_time, self.start_time )
        repeat_end     = self.repeat_end or datetime.now() + relativedelta( years = 1 )
        dates          = []

        if self.repeat_interval is EventRepeat.Once:
            dates = [ start_time ]
        elif self.repeat_interval is EventRepeat.MonthlyByDayOfWeek:
            dates = list(rrule( self.repeat_interval, dtstart=self.start_time, until=repeat_end, byweekday=self.start_time.weekday() ))
        else:
            dates = list(rrule( self.repeat_interval, dtstart=self.start_time, until=repeat_end ))

        for dt in dates:
            self.create_instance(dt,dt + end_time_delta )

        db.session.commit()

    def create_instance(self,start_time,end_time):
        return EventDateInstance.create({
            start_time:    start_time,
            end_time:      end_time,
            event_id:      self.event_id,
            event_date_id: self.id
        })

    def destroy_instances(self, **kwargs ):

        query = EventDateInstance.query.filter( EventDateInstance.event_date_id == self.id )

        if ( kwargs['fromNow'] ):
          query = query.filter( EventDateInstance.start_time >= datetime.now() )

        query.delete(synchronize_session=False)


class EventDateInstance(Model,Base):
    __tablename__ = 'events_date_instances'

    event_id        = Column( UUID(as_uuid=True), ForeignKey('events.id') )
    event_date_id   = Column( UUID(as_uuid=True), ForeignKey('events_dates.id') )
    start_time      = Column( DateTime )
    end_time        = Column( DateTime )

    event      = relationship("Event")
    event_date = relationship("EventDate")

# for translatable parts of the event
class EventInfo(TranslationModel,Base):
    __tablename__ = 'events_i18n'

    id          = Column( UUID(as_uuid=True), ForeignKey('events.id'), primary_key=True )
    title       = Column( Text )
    description = Column( Text )
    accessibility_information = Column( Text )

    event = relationship( "Event" )

