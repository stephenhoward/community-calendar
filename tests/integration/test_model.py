
from event_calendar.config import config


import unittest
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from event_calendar.model import Model
from event_calendar.database import DB, Base

db = DB()

class ChildModel(Model,Base):

    __tablename__ = 'child_models'

    name      = Column(String)
    parent_id = Column( UUID(as_uuid=True), ForeignKey("parent_models.id") )
    parent    = relationship("ParentModel")

class ParentModel(Model,Base):

    __tablename__ = 'parent_models'

    name     = Column(String)
    children = relationship( "ChildModel", back_populates="parent" )

class TestModel(unittest.TestCase):

    def setUp(self):

        config.set(['db','database'],'test_model')
        db.build_engine()
        db.create_db()

    def tearDown(self):
        db.destroy_db()

    def test_round_trip(self):
        model = ParentModel.create({ 'name': 'Foo' })
        ret = model.save()
        assert( ret == model )
        model2 = ParentModel.get(model.id)
        assert( model2 == model )

    def test_complex_round_trip(self):
        model = ParentModel.create({
            "name": "FOO"
        })
        model.children = [
            ChildModel.create({ "name": "BAR" }),
            ChildModel.create({ "name": "BAZ" })
        ]

        ret = model.save()
        assert( ret == model )
        model2 = ParentModel.get(model.id)
        assert( model2 == model )
        assert( len(model2.children) == 2 )

    def test_simple_search(self):
        model   = ParentModel.create({ 'name': 'Bar' }).save()
        model2  = ParentModel.create({ 'name': 'Baz' }).save()

        models  = ParentModel.search( ParentModel.name == 'Gone' )
        assert( len(models.all()) == 0 )

        models  = ParentModel.search( ParentModel.name == 'Bar' )
        assert( len(models.all()) == 1 )


if __name__ == '__main__':
    unittest.main()
