import unittest
from unittest.mock import patch
from event_calendar.model import Model, Translation
import event_calendar.model
from event_calendar.database import db_session
from uuid import uuid4 as uuid



class TestCodes(unittest.TestCase):

    def test_codes_exist(self):
        assert( 'en' in event_calendar.model.LanguageCode.__members__ )

class TestModel(unittest.TestCase):

    def test_create(self):
        id = uuid()
        with patch.object( db_session, 'add', return_value = True ):
            model = Model.create( { 'id': id } )
            assert( model.id == id )

    def update(self):
        id = uuid()
        model = Model( id = id )
        assert( model.id == id )
        id2 = uuid()
        model.update({ id: id2 })
        assert( model.id == id2 )

    def test_get(self):
        id = uuid()
        with patch.object( db_session, 'query', return_value = Model( id = id ) ):
            model = Model.get(id)
            assert( model.id == id )

    def save(self):
        id = uuid()
        with patch.object( db_session, 'commit', return_value = True ):
            model = Model( id = id )


if __name__ == '__main__':
    unittest.main()