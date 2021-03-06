from event_calendar.config import config
from event_calendar.model.user import User
from app import create_app
from sqlalchemy.orm import Query
from uuid import UUID, uuid4 as uuid
from event_calendar.database import DB
from event_calendar.testing.test_client import TestClient
import unittest

db = DB()

test_user = {
    "email": "testing@example.com",
    "password": "baddpassword"
}

bad_credentials = {
    "email": "bad@example.com",
    "password": "badpassword"
}

class TestAPI(unittest.TestCase):


    def setUp(self):
        config.set(['db','database'],'test_auth')
        db.build_engine()
        db.create_db()

        app = create_app();
        app.test_client_class = TestClient
        self.client = app.test_client()

    def tearDown(self):
        db.destroy_db()

    def test_post_nologin(self):
        res = self.client.post('/v1/events')
        assert(res.status_code == 401 )

    def test_post_firstlogin(self):
        res = self.client.post('/v1/auth/token', json = test_user )
        assert(res.status_code == 200 )

    def test_post_badlogin(self):
        user = User.create(test_user)
        user.save()
        res = self.client.post('/v1/auth/token', json = bad_credentials )
        assert(res.status_code == 401 )

    def test_post_goodlogin(self):
        jwt = None

        with self.subTest('login'):
            res  = self.client.login()
            assert(res.status_code == 200 )
            assert(res.mimetype == 'text/plain' )
            assert(len(res.data) > 0 )
            jwt = res.data.decode('ascii')

        with self.subTest('refresh token'):
            res = self.client.get('/v1/auth/token', headers = { 'Authorization': 'Bearer ' + jwt })
            assert(res.status_code == 200 )
            assert(res.mimetype == 'text/plain' )
            assert(len(res.data) > 0 )

    def test_bad_tokenrefresh(self):
        res = self.client.get('/v1/auth/token')
        assert(res.status_code == 401 )

        res = self.client.get('/v1/auth/token', headers = { 'Authorization': 'Bearer nonsense' })
        assert(res.status_code == 401 )

if __name__ == '__main__':
    unittest.main()
