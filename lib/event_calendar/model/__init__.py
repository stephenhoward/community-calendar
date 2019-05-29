from sqlalchemy import Column, Enum
from sqlalchemy.dialects.postgresql import UUID as UUIDColumn
from event_calendar.database import db_session
import enum
import yaml
from uuid import UUID, uuid4 as uuid

codes  = yaml.load( open('config/language_codes.yaml','r'), Loader=yaml.FullLoader )

LanguageCode = enum.Enum( 'LanguageCode', codes['LanguageCode']['enum'] )

class Model(object):
    id = Column( UUIDColumn, primary_key=True )

    def __init__(self,**kwargs):
        self.update(kwargs)

        if ( not isinstance( self.id, UUID ) ):
            self.id = uuid()

    @classmethod
    def get(cls,id):
        return db_session.query( cls ). \
            filter(cls.id == id). \
            one()

    @classmethod
    def create(cls,dict):
        model = cls(**dict)
        db_session.add(model)
        return model

    def update(self,dict):
        for key, value in dict.items():
            setattr( self, key, value )
        return self

    def save(self):
        db_session.commit()
        return self

class Translation(Model):
    language = Column( Enum(LanguageCode), primary_key=True )
