import unittest
from app import create_app
from unittest.mock import patch
from event_calendar.config import config
from event_calendar.database import DB
from event_calendar.testing.test_client import TestClient
from werkzeug.exceptions import Forbidden
from uuid import UUID, uuid4 as uuid

db = DB()

class TestApiGuards(unittest.TestCase):

    def setUp(self):
        config.set(['db','database'],'test_guards')
        db.build_engine()
        db.create_db()

        app = create_app();
        app.test_client_class = TestClient
        self.client = app.test_client()

    def tearDown(self):
        db.destroy_db()

    def test_unauthenticated(self):
        res = self.client.post( '/v1/events', json = { "org_id": uuid(), "info" : [ { "language": "en", "title": "5k Fun Race" } ] }  )
        self.assertEqual( res.status_code, 401 )

    def test_unauthorized(self):
        self.client.login()
        res = self.client.post( '/v1/events', json = { "org_id": uuid(), "info" : [ { "language": "en", "title": "5k Fun Race" } ] }  )
        self.assertEqual( res.status_code, 403 )

if __name__ == '__main__':
    unittest.main()
