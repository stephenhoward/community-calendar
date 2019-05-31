import unittest
from unittest.mock import patch
from event_calendar.model import Model
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID as UUIDColumn
from sqlalchemy.orm import relationship
import event_calendar.model
from event_calendar.database import DB, Base
from uuid import UUID, uuid4 as uuid

db = DB()

class TestCodes(unittest.TestCase):

    def test_codes_exist(self):
        assert( 'en' in event_calendar.model.LanguageCode.__members__ )
        assert( 'es' in event_calendar.model.LanguageCode.__members__ )
        assert( 'fr' in event_calendar.model.LanguageCode.__members__ )

class ChildModel(Model,Base):

    __tablename__ = 'child_models'

    name      = Column(String)
    parent_id = Column( UUIDColumn(as_uuid=True), ForeignKey("parent_models.id") )
    parent    = relationship("ParentModel")

class ParentModel(Model,Base):

    __tablename__ = 'parent_models'

    name     = Column(String)
    children = relationship( "ChildModel", back_populates="parent" )

class TestModel(unittest.TestCase):

    def test_create(self):
        id = uuid()
        with patch.object( db.session, 'add', return_value = True ):
            model = ParentModel.create( { 'id': id } )
            assert( isinstance(model,Model) )
            assert( model.id == id )
            model_no_id = ParentModel.create( {} )
            assert( isinstance(model_no_id,Model) )
            assert( isinstance(model_no_id.id, UUID ) )

    def test_update(self):
        id = uuid()
        model = ParentModel( id = id )
        assert( model.id == id )
        id2 = uuid()
        ret = model.update({ 'id': id2 })
        assert( model.id == id2 )
        assert( ret == model )

    def test_complex_create_with_dict(self):
        model = ParentModel.create({
            "name": "FOO",
            "children":[
                { "name": "BAR" },
                { "name": "BAZ" }
            ]
        })

    def test_complex_create_with_mixed(self):
        model = ParentModel.create({
            "name": "FOO",
            "children":[
                ChildModel.create({ "name": "BAR" }),
                { "name": "BAZ" }
            ]
        })

    def test_save(self):
        id = uuid()
        with patch.object( db.session, 'commit', return_value = True ):
            model = ParentModel( id = id )
            ret = model.save()
            assert( model.id == id )
            assert( ret == model )

if __name__ == '__main__':
    unittest.main()