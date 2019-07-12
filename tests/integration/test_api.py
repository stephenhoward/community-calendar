import sys

sys.path.append('/opt/calendar')

import unittest
from app import create_app
from unittest.mock import patch
from sqlalchemy.orm import Query
from event_calendar.model.event import Event
from uuid import UUID, uuid4 as uuid

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = create_app().test_client()

    def test_spec(self):
        res = self.client.get('/v1/openapi.json')
        assert(res.status_code == 200 )

    def test_events_search(self):
        with patch.object( Query, 'all', return_value = [
            { 'id': uuid() }
        ]):
            res = self.client.get('/v1/events')
            assert(res.status_code == 200 )

    def test_event_get(self):
        id = uuid()
        print('/v1/events/' + str(id) )
        with patch.object( Query, 'one', return_value = { 'id': id } ):
            res = self.client.get('/v1/events/' + str(id) )
            assert(res.status_code == 200 )

if __name__ == '__main__':
    unittest.main()
