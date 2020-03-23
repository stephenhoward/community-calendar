from sqlalchemy import Column, Table, String, Text, Enum, Boolean, DateTime, ForeignKey, tuple_
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr,declarative_base
from sqlalchemy.dialects.postgresql import UUID
import enum
from event_calendar.model import Model
from event_calendar.database import Base
import event_calendar.model.user
import event_calendar.model.event
import event_calendar.model.series

TargetClasses = enum.Enum( 'TargetClass', [
    'Event',
    'Series',
    'Location'
])


# for internal discussion of drafted content:
class BaseComment(Model):

    when      = Column( DateTime )
    edited    = Column( Boolean )
    contents  = Column( Text )

    @declared_attr
    def author_id(cls):
        return Column( UUID(as_uuid=True), ForeignKey('users.id') )

    @declared_attr
    def author(cls):
        return relationship( "User" )

class Comment(BaseComment,Base):

    __tablename__ = 'content_comments'

    target_id = Column( UUID(as_uuid=True) )
    target_class = Column( Enum(TargetClasses) )
    target_anchor = Column( String )
    resolved = Column( Boolean )
    replies = relationship( "Reply", lazy='joined' )

class Reply(BaseComment,Base):

    __tablename__ = 'content_replies'

    parent_id = Column( UUID(as_uuid=True), ForeignKey('content_comments.id') )
