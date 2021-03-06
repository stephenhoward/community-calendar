import unittest
from app import create_app
from unittest.mock import patch
from sqlalchemy.orm import Query
from event_calendar.model.content import ContentStatus
from event_calendar.model.event import Event
from uuid import UUID, uuid4 as uuid

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = create_app().test_client()

    def test_spec(self):
        res = self.client.get('/v1/openapi.json')
        self.assertEqual(res.status_code, 200 )

    def test_events_search(self):
        with patch.object( Query, 'all', return_value = [
            { 'id': uuid() }
        ]):
            res = self.client.get('/v1/events')
            self.assertEqual(res.status_code, 200 )

    def test_event_get_unpublished(self):
        id = uuid()
        with patch.object( Query, 'one', return_value = Event.create({ 'id': id }) ):
            res = self.client.get('/v1/events/' + str(id) )
            self.assertEqual(res.status_code, 404 )

    def test_event_get(self):
        id = uuid()
        with patch.object( Query, 'one', return_value = Event.create({ 'id': id, 'status': ContentStatus.Active }) ):
            res = self.client.get('/v1/events/' + str(id) )
            self.assertEqual(res.status_code, 200 )

if __name__ == '__main__':
    unittest.main()
