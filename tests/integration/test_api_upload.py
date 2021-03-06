import sys
import io
from event_calendar.config import config
from event_calendar.database import DB
from event_calendar.testing.test_client import TestClient
from flask import url_for

sys.path.append('/opt/calendar')

import unittest
from app import create_app
from unittest.mock import patch

from event_calendar.model.event import Event
from uuid import UUID, uuid4 as uuid
from werkzeug.datastructures import FileStorage

db = DB()

class TestApiUpload(unittest.TestCase):

    def setUp(self):
        config.set(['db','database'],'test_auth')
        db.build_engine()
        db.create_db()

        app = create_app();
        app.test_client_class = TestClient
        self.client = app.test_client()

    def test_site_image_upload(self):
        self.client.login()
        data = {}
        data['file'] = (io.BytesIO(b"abcdef"), 'test.jpg')
        with patch.object( FileStorage, 'save' ):
            res = self.client.post(
                '/v1/site/image', #url_for('site.post_image'),
                data         = data,
                content_type = 'multipart/form-data'
            )
            assert(res.status_code == 200 )
            assert(res.is_json)
            assert( 'filename' in res.get_json() )

if __name__ == '__main__':
    unittest.main()
