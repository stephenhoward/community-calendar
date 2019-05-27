from sqlalchemy import Column, Enum
from sqlalchemy.dialects.postgresql import UUID
from event_calendar.database import db_session
import enum
import yaml

codes  = yaml.load( open('config/language_codes.yaml','r'), Loader=yaml.FullLoader )

LanguageCode = enum.Enum( 'LanguageCode', codes['LanguageCode']['enum'] )

class Model(object):
    id = Column( UUID, primary_key=True )

    def get(id):
        return db_session.query( type(self) ).filter(type(self).id == id).one()

    def create(dict):
        model = type(self)(**dict)
        db_session.add(model)
        return model

    def update(dict):
        for key, value in dict.items():
            setattr( self, key, value )
        return self

    def save():
        db_session.commit()
        return self

class Translation(Model):
    language = Column( Enum(LanguageCode), primary_key=True )
