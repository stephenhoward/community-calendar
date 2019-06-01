import unittest
from app import create_app

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = create_app().test_client()

    def test_spec(self):
        res = self.client.get('/v1/openapi.json')
        assert(res.status_code == 200 )

    def test_events_get(self):
        res = self.client.get('/v1/events')
        assert(res.status_code == 200 )
