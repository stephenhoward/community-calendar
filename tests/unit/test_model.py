import unittest
from unittest.mock import patch
from event_calendar.model import Model
import event_calendar.model
from event_calendar.database import DB
from uuid import UUID, uuid4 as uuid

db = DB()

class TestCodes(unittest.TestCase):

    def test_codes_exist(self):
        assert( 'en' in event_calendar.model.LanguageCode.__members__ )
        assert( 'es' in event_calendar.model.LanguageCode.__members__ )
        assert( 'fr' in event_calendar.model.LanguageCode.__members__ )

class TestModel(unittest.TestCase):

    def test_create(self):
        id = uuid()
        with patch.object( db.session, 'add', return_value = True ):
            model = Model.create( { 'id': id } )
            assert( isinstance(model,Model) )
            assert( model.id == id )
            model_no_id = Model.create( {} )
            assert( isinstance(model_no_id,Model) )
            assert( isinstance(model_no_id.id, UUID ) )

    def test_update(self):
        id = uuid()
        model = Model( id = id )
        assert( model.id == id )
        id2 = uuid()
        ret = model.update({ 'id': id2 })
        assert( model.id == id2 )
        assert( ret == model )

    def test_save(self):
        id = uuid()
        with patch.object( db.session, 'commit', return_value = True ):
            model = Model( id = id )
            ret = model.save()
            assert( model.id == id )
            assert( ret == model )

if __name__ == '__main__':
    unittest.main()