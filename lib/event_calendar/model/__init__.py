from sqlalchemy import create_engine, Column, String, Enum, Text, LargeBinary, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
import enum
import yaml

engine = create_engine('postgresql://postgres@localhost:5432/events_calendar')
codes  = yaml.load( open('config/language_codes.yaml','r'), Loader=yaml.FullLoader )

LanguageCode = enum.Enum( 'LanguageCode', codes['LanguageCode']['enum'] )

class Model(object):
    id = Column( UUID, primary_key=True )

class Translation(Model):
    language = Column( Enum(LanguageCode), primary_key=True )
