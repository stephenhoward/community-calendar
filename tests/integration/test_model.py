
from event_calendar.config import config


import unittest
from sqlalchemy import Column, String
from event_calendar.model import Model
from event_calendar.database import DB, Base

db = DB()

class StoredModel(Model,Base):
    __tablename__ = 'stored_models'

    name = Column(String)

class TestModel(unittest.TestCase):

    def setUp(self):

        config.set(['db','database'],'test_model')
        db.build_engine()
        db.create_db()

    def tearDown(self):
        db.destroy_db()

    def test_round_trip(self):
        model = StoredModel.create({ 'name': 'Foo' })
        ret = model.save()
        assert( ret == model )
        model2 = StoredModel.get(model.id)
        assert( model2 == model )

if __name__ == '__main__':
    unittest.main()
