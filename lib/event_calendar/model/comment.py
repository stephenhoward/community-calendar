from sqlalchemy import Column, Table, String, Text, Enum, Boolean, DateTime, ForeignKey, tuple_
from sqlalchemy.orm import relationship, backref
from sqlalchemy.dialects.postgresql import UUID
import enum
from event_calendar.model import Model
from event_calendar.database import Base
import event_calendar.model.user
import event_calendar.model.event
import event_calendar.model.series

# for internal discussion of drafted content:
class Comment(Model):

    id        = Column( UUID(as_uuid=True), primary_key=True )
    when      = Column( DateTime )
    edited    = Column( Boolean )
    author_id = Column( UUID(as_uuid=True), ForeignKey('users.id') )
    contents  = Column( Text )

    author    = relationship( "User" )

class EventComment(Model,Base):

    __tablename__ = 'event_comments'
    event_id  = Column( UUID(as_uuid=True), ForeignKey('events.id') )
    parent_id = Column( UUID(as_uuid=True), ForeignKey('event_comments.id') )
    children  = relationship( "EventComment", backref=backref("parent", remote_side='EventComment.id')  )
    event     = relationship( "Event", back_populates="comments" )

class SeriesComment(Model,Base):

    __tablename__ = 'series_comments'
    series_id = Column( UUID(as_uuid=True), ForeignKey('series.id') )
    parent_id = Column( UUID(as_uuid=True), ForeignKey('series_comments.id') )
    children  = relationship( "SeriesComment", backref=backref("parent", remote_side='SeriesComment.id')  )
    series    = relationship( "Series", back_populates="comments" )