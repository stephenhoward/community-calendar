from sqlalchemy import Column, Table, Text, Enum, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

event_categories_table = Table('event_categories', Base.metadata,
    Column('event_id',    UUID, ForeignKey('events.id')),
    Column('category_id', UUID, ForeignKey('categories.id'))
)

class EventStatus(enum.Enum):
    Draft  = 1
    Active = 2

class EventRepeat(enum.Enum):
    Daily   = 1
    Weekly  = 2
    Monthly = 3

class EventRepeatBy(enum.Enum):
    DayOfMonth      = 1  # 12th of each month
    WeekdayOfMonth  = 2  # First Tuesday of each month

class Event(Base):
    __tablename__ = 'events'

    id         = Column( UUID, primary_key=True )
    status     = Column( Enum(EventStatus) )
    start      = Column( DateTime )
    end        = Column( DateTime )
    dates_only = Column( Boolean )
    repeat     = Column( Enum(EventRepeat) )
    repeat_by  = Column( Enum(EventRepeatBy) )
    info       = relationship( "EventInfo", back_populates="event" )
    categories = relationship( "Event", secondary="event_categories_table" )
    images     = relationship( "Image" )
    events     = relationship( "Event" )
    comments   = relationship( "EventComment", back_populates="event" )

# for translatable parts of the event
class EventInfo(Base):
    __tablename__ = 'events_i18n'

    id          = Column( UUID,    primary_key=True, ForeignKey('events.id') )
    language    = Column( VarChar, primary_key=True )
    title       = Column( Text )
    description = Column( Text )

    event = relationship( "Event", back_populates="info" )

# for internal discussion of drafted events:
class EventComment(Base):
    __tablename__ = 'event_comments'

    id        = Column( UUID, primary_key = True )
    when      = Column( DateTime )
    edited    = Column( Boolean )
    event_id  = Column( UUID, ForeignKey('events.id') )
    author_id = Column( UUID, ForeignKey('users.id') )
    parent_id = Column( UUID, ForeignKey('event_comments.id') )
    contents  = Column( Text )
    event          = relationship( "Event" )
    author         = relationship( "User" )
    parent_comment = relationship( "EventComment" )
    child_comments = relationship( "EventComment" )

