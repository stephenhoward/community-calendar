from sqlalchemy import Column, String, Text, Enum, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.dialects.postgresql import UUID
import enum
from event_calendar.model import Model
from event_calendar.database import Base
from event_calendar.model.user import User

TargetClasses = enum.Enum( 'TargetClass', [
    'Event',
    'Series',
    'Location'
])

# for internal discussion of drafted content:
class BaseComment(Model):

    create_time = Column( DateTime )
    edited      = Column( Boolean )
    contents    = Column( Text )

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

    comment_id = Column( UUID(as_uuid=True), ForeignKey('content_comments.id') )

class CommentableMixin (object):

    def get_comments(self):
        return Comment.search(
            target_class == self.__class__.__name__,
            target_id    == self.id
        ).all()

    def add_comment(self,json):
        if ( 'comment_id' in json ):
            comment = Comment.get( json['comment_id'] )
            if ( comment ):
                reply = Reply.create(json).save()
                return reply
            else:
                raise Exception( 'no parent comment found for reply' )
        else:
            json['target_class'] = self.__class__.__name__
            json['target_id']    = self.id

            comment = Comment.create(json).save()
            return comment
