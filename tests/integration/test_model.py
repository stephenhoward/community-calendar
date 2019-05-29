import unittest
from sqlalchemy import Column, String
from event_calendar.model import Model
from event_calendar.database import Base, engine

class StoredModel(Model,Base):
    __tablename__ = 'stored_models'

    name = Column(String)

class TestModel(unittest.TestCase):

    def setUp(self):
        Base.metadata.create_all(engine)

    def tearDown(self):
        Base.metadata.drop_all(engine)

    def test_round_trip(self):
        model = StoredModel.create({ 'name': 'Foo' })
        ret = model.save()
        assert( ret == model )
        model2 = StoredModel.get(model.id)
        assert( model2 == model )

if __name__ == '__main__':
    unittest.main()
