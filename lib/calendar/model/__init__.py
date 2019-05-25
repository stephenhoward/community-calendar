from sqlalchemy import create_engine, Column, String, Text, LargeBinary, ForeignKey
from sqlalchemy.dialects.postgresql import UUID


engine = create_engine('postgresql://postgres@localhost:5432/events_calendar')

class Model(object):
    id   = Column( UUID, primary_key=True )

class Translation(Model):
    language    = Column( String, primary_key=True )
