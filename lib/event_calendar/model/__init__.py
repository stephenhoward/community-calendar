from sqlalchemy import Column, Enum
from sqlalchemy.dialects.postgresql import UUID as UUIDColumn
from event_calendar.database import DB
import enum
import yaml
from uuid import UUID, uuid4 as uuid

db    = DB()
codes = yaml.load( open('config/language_codes.yaml','r'), Loader=yaml.FullLoader )

LanguageCode = enum.Enum( 'LanguageCode', codes['LanguageCode']['enum'] )

class Model(object):
    id = Column( UUIDColumn(as_uuid=True), primary_key=True )

    def __init__(self,**kwargs):
        self.update(kwargs)

        if ( not isinstance( self.id, UUID ) ):
            self.id = uuid()

    @classmethod
    def get(cls,id):
        return db.session.query( cls ). \
            filter(cls.id == id). \
            one()

    @classmethod
    def create(cls,dict):
        model = cls(**dict)
        db.session.add(model)
        return model

    def update(self,dict):
        for key, value in dict.items():
            setattr( self, key, value )
        return self

    def save(self):
        db.session.commit()
        return self

class Translation(Model):
    language = Column( Enum(LanguageCode), primary_key=True )
