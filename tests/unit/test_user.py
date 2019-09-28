from event_calendar.config import config
from event_calendar.model.user import User
from unittest.mock import patch
from sqlalchemy.orm import Query
from uuid import UUID, uuid4 as uuid
from event_calendar.database import DB, Base
import pprint
import unittest

db = DB()

test_user = {
    "email": "test@example.com",
    "password": "baddpassword"
}

class TestAPI(unittest.TestCase):

    def test_password(self):
        user = User.create(test_user)
        assert( print(user.password) != test_user['password'] )
        assert( not user.check_password( 'wrong_password' ) )
        assert( user.check_password( test_user['password'] ) )

if __name__ == '__main__':
    unittest.main()
