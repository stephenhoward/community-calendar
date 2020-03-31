import unittest
from unittest.mock import patch, Mock
from uuid import UUID, uuid4 as uuid
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, Query
from event_calendar.database import DB, Base
from event_calendar.model.comment import Model
from event_calendar.model.comment import Comment,CommentableMixin,Reply

class ContentMod(CommentableMixin,Model,Base):

    __tablename__ = 'commentable_models'

    name = Column(String)

class TestModelComments(unittest.TestCase):


    @patch('event_calendar.model.db.session')
    def test_add_comment(self,mock_session):
        mock_session.add.return_value    = True
        mock_session.commit.return_value = True

        comment_data = {
            'contents': 'this is the body',
            'author_id': uuid()
        }
        model = ContentMod.create( { 'id': uuid() } )
        assert( isinstance(model,CommentableMixin) )
        comment = model.add_comment( comment_data )
        assert( isinstance(comment, Comment ) )
        assert( comment.target_id == model.id )
        assert( comment.target_class == model.__class__.__name__ )

    @patch('event_calendar.model.db.session')
    def test_add_bad_reply(self,mock_session):
        mock_session.add.return_value    = True
        mock_session.commit.return_value = True

        reply_data = {
            'contents': 'this is the body',
            'author_id': uuid(),
            'parent_id': uuid()
        }
        model = ContentMod.create( { 'id': uuid() } )
        self.assertRaises( Exception, model.add_comment, reply_data )

    # TODO
    # @patch('event_calendar.model.db.session')
    # def test_add_good_reply(self,mock_session):
    #     mock_session.add.return_value    = True
    #     mock_session.commit.return_value = True

    #     reply_data = {
    #         'contents': 'this is the body',
    #         'author_id': uuid(),
    #         'parent_id': uuid()
    #     }
    #     model = ContentMod.create( { 'id': uuid() } )
    #     reply = model.add_comment( reply_data )
    #     assert( isinstance( reply, Reply ) )

if __name__ == '__main__':
    unittest.main()