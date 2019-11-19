import unittest
from unittest.mock import patch
import datetime
from event_calendar.database import DB
from event_calendar.model.password_token import PasswordToken
from sqlalchemy.orm import Query
from event_calendar.model.user import User

db = DB()

class TestConfig(unittest.TestCase):

    def test_generate(self):
        with patch.object( db.session, 'commit', return_value = True ):
            user = User.create({ 'email': 'test@example.com' })

            with patch.object( Query, 'first', return_value = None ):
                token = PasswordToken.generate(user)

                assert( isinstance( token, PasswordToken ) )
                assert( token.user_id == user.id )
                assert( token.expires > datetime.datetime.utcnow() )

    def test_generate_existing(self):
        with patch.object( db.session, 'commit', return_value = True ):
            with patch.object( Query, 'first', return_value = None ):
                user             = User.create({ 'email': 'test@example.com' })
                token            = PasswordToken.generate(user)
                token_dict       = token.dump()
                token_dict['id'] = token.id

                with patch.object( Query, 'first', return_value = token_dict ):
                    token2 = PasswordToken.generate(user)

                    assert( token.id == token2.id )

    def test_expire(self):

        with patch.object( db.session, 'commit', return_value = True ):
            user = User.create({ 'email': 'test@example.com' })

            with patch.object( Query, 'first', return_value = None ):
                token = PasswordToken.generate(user)
                token.expire()

                assert( token.expires <= datetime.datetime.utcnow() )

if __name__ == '__main__':
    unittest.main()
