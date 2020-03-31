import unittest
from unittest.mock import patch
from uuid import UUID, uuid4 as uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as UUIDColumn
from sqlalchemy.orm import relationship
from event_calendar.model import Model
from event_calendar.database import DB, Base

db = DB()

class ChildMod(Model,Base):

    __tablename__ = 'child_mods'

    name      = Column(String)
    parent_id = Column( UUIDColumn(as_uuid=True), ForeignKey("parent_mods.id") )
    parent    = relationship("ParentMod")

class ParentMod(Model,Base):

    __tablename__ = 'parent_mods'

    name     = Column(String)
    children = relationship( "ChildMod", back_populates="parent" )

class TestModel(unittest.TestCase):

    def test_create(self):
        id = uuid()
        with patch.object( db.session, 'add', return_value = True ):
            model = ParentMod.create( { 'id': id } )
            assert( isinstance(model,Model) )
            assert( model.id == id )
            model_no_id = ParentMod.create( {} )
            assert( isinstance(model_no_id,Model) )
            assert( isinstance(model_no_id.id, UUID ) )

    def test_dump(self):
        params = {
          'id': uuid(),
          'name': 'dumped'
        }
        model = ParentMod.create(params)
        self.assertDictEqual( params, model.dump() )

    def test_update(self):
        id = uuid()
        model = ParentMod( id = id )
        assert( model.id == id )
        id2 = uuid()
        ret = model.update({ 'id': id2 })
        assert( model.id == id2 )
        assert( ret == model )

    def test_save(self):
        id = uuid()
        with patch.object( db.session, 'commit', return_value = True ):
            model = ParentMod( id = id )
            ret = model.save()
            assert( model.id == id )
            assert( ret == model )

if __name__ == '__main__':
    unittest.main()